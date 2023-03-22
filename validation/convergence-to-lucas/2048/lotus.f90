program swimming_plate
  use bodyMod,    only: body
  use fluidMod,   only: fluid
  use mympiMod,   only: init_mympi,mympi_end,mympi_rank
  use gridMod,    only: xg,composite
  use imageMod,   only: display
  use geom_shape
  use uMod,       only: avrgField
  implicit none
!
! -- Physical parameters
  real,parameter     :: Re = 77000
!
  real,parameter     :: c=2048, nu=c/Re
  real, parameter    :: finish=8
  integer            :: b(3) = [16,8,1]
!
! -- Hyperparameters
  real, parameter    :: thicc=0.03*c
  real, parameter    :: A = 0.1*c, St_d = 0.31009362717481354, k_x=0., k_z=16.0, h_roughness=0.0
  real, parameter    :: coeffs(3) = [0.072, 0.1685, -0.0701] ! lowest power first
  real, parameter    :: k_coeff = 1/2.15, f = St_d/(2.*(sum(coeffs))*c)
!
! -- Dimensions
  integer            :: n(3), ndims=2
!
! -- Setup solver
  logical            :: there = .false., root, p(3) = [.FALSE.,.FALSE.,.TRUE.]
  real               :: m(3), z
  type(fluid)        :: flow
  type(body)         :: geom
!
!
! -- Outputs
  real            :: dt, t, pforce(3), vforce(3), ppower(3)
!
! -- Initialize
  call init_mympi(ndims,set_blocks=b(1:ndims),set_periodic=p(1:ndims))
  root = mympi_rank()==0
  if(root) print *,'Setting up the grid, body and fluid'
  if(root) print *,'-----------------------------------'
!
! -- Setup the grid
  if(ndims==2) then
    z = 0.0
  else
    z = 8./(k_z*4.)
  end if
  m = [1.5,1.5, z]
  n = composite(c*m,prnt=root)
  call xg(1)%stretch(n(1), -2.0*c, -.5*c, 2.5*c, 7.0*c,  h_min=4., h_max=10., prnt=root)
  call xg(2)%stretch(n(2), -2.0*c, -0.9*c, 0.9*c, 2.0*c, h_min=2., prnt=root)
  if(ndims==3) xg(3)%h = 4.
!
! -- Call the geometry and kinematics

  geom = wavy_wall(c, thicc).and.upper(c,thicc).and.lower(c,thicc).map.init_warp(2,h,doth,dh)
!
! -- Initialise fluid
  call flow%init(n/b,geom,V=[1.,0.,0.],nu=nu,exit=.true.)
  ! call avrg%init(flow)
  flow%time = 0
!
  if(root) print *,'Starting time update loop'
  if(root) print *,'-----------------------------------'
!
  time_loop: do while (flow%time<finish/f.and..not.there)
    t = flow%time
    dt = flow%dt
    call geom%update(t+dt) ! update geom
    call flow%update(geom)

    write(9,'(f10.4,f8.4,4e16.8,4e16.8,4e16.8,4e16.8,4e16.8,4e16.8,&
          4e16.8,4e16.8,4e16.8,4e16.8,4e16.8,4e16.8,4e16.8,4e16.8)')&
          t*f,dt,pforce,ppower,vforce

    pforce = 2.*geom%pforce(flow%pressure)/(c*n(3)*xg(3)%h)
    ppower = 2.*geom%ppower(flow%pressure)/(c*n(3)*xg(3)%h)
    vforce = 2.*nu*geom%vforce_f(flow%velocity)/(A*n(3)*xg(3)%h)

    if((mod(t,1./f)<dt).and.(root)) print "('Time:',f15.3,'. Thrust:',f15.3,3f12.6)",&
    t*f, (pforce(1)+vforce(1))

    inquire(file='../.kill', exist=there)
    if (there) exit time_loop

    ! if((t>(finish-4)/f).and.(mod(t,0.1/f)<dt)) call flow%write(geom, write_vtr=.false.)

  end do time_loop

  if(root) print *,'Loop complete: writing restart files and exiting'
  if(root) print *,'-----------------------------------'
!     call flow%write(geom, write_vtr=.false.)
  call mympi_end
contains
!
type(set) function wavy_wall(length, thickness) result(geom)
  real,intent(in) :: length, thickness
  geom = plane([1.,-0.,0.],[length,0.,0.]) & ! end cap
  .and.plane([-1.,0.,0.],[0.,0.,0.]) ! front cap
end function
!
type(set) function upper(length, thickness) result(geom)
  real,intent(in) :: length, thickness
  geom = plane([0.,1.,0.],[0.,0.5*thickness,0.])&
  .map.init_warp(2,egg_top,dotegg_top,degg_top)
end function
!
type(set) function lower(length, thickness) result(geom)
  real,intent(in) :: length, thickness
  geom = plane([-0.,-1.,0.],[0.,-0.5*thickness,0.])&
  .map.init_warp(2,egg_bottom,dotegg_bottom,degg_bottom)
end function
!
! -- General kinematics
real pure function h(x)
  real,intent(in) :: x(3)
  h = amp(x(1))*sin(arg(x(1)))
end function h
real pure function doth(x)
  real,intent(in) :: x(3)
  doth = amp(x(1))*cos(arg(x(1)))*2*pi*f
end function doth
pure function dh(x)
  real,intent(in) :: x(3)
  real            :: dh(3)
  dh = 0
  dh(1) = damp(x(1))*sin(arg(x(1))) &
        - amp(x(1))*cos(arg(x(1)))*2*pi*k_coeff/c
end function dh
real pure function arg(x)
  real,intent(in) :: x
  real :: xp
  xp = min(max(x/c,0.),1.)
  arg = (2*pi*(f*flow%time - k_coeff*xp))
end function arg
real pure function amp(x)
  real,intent(in) :: x
  real    :: xp
  integer :: n
  xp = min(max(x/c,0.),1.)
  amp=0*xp
  do concurrent (n=1:size(coeffs))
    amp = amp + c*(coeffs(n)*(xp**(n-1)))
  end do
end function amp
real pure function damp(x)
  real,intent(in) :: x
  real    :: xp
  integer :: n
  xp = min(max(x/c,0.),1.)
  damp=0*xp
  do concurrent (n=2:size(coeffs))
    damp = damp + coeffs(n)*(n-1)*(xp**(n-2))
  end do
end function damp
!
! -- Egg carton roughness distribution
real pure function egg_top(x)
  real,intent(in) :: x(3)
  egg_top = (h_roughness*c)*sin((k_x)*(2*pi*x(1)/c)-pi/2)*cos((k_z)*(2*pi*x(3)/c))
end function egg_top
pure function degg_top(x)
  real,intent(in) :: x(3)
  real            :: degg_top(3)
  degg_top = 0
  degg_top(1) = (h_roughness*c)*cos((k_x)*(2*pi*x(1)/c)-pi/2)&
                                *sin((k_z)*(2*pi*x(3)/c))*(k_x)*(2*pi/c)
  degg_top(3) = -(h_roughness*c)*cos((k_x)*(2*pi*x(1)/c-pi/2))&
                                *sin((k_z)*(2*pi*x(3)/c))*(k_z)*(2*pi/c)
end function degg_top
real pure function dotegg_top(x)
  real,intent(in) :: x(3)
  dotegg_top = 0
end function dotegg_top
!
real pure function egg_bottom(x)
  real,intent(in) :: x(3)
  egg_bottom = (h_roughness*c)*sin((k_x)*(2*pi*x(1)/c)-3*pi/2)&
                               *cos((k_z)*(2*pi*x(3)/c))
end function egg_bottom
pure function degg_bottom(x)
  real,intent(in) :: x(3)
  real            :: degg_bottom(3)
  degg_bottom = 0
  degg_bottom(1) = (h_roughness*c)*cos((k_x)*(2*pi*x(1)/c)-3*pi/2)&
                                   *sin((k_z)*(2*pi*x(3)/c))*(k_x)*(2*pi/c)
  degg_bottom(3) = -(h_roughness*c)*cos((k_x)*(2*pi*x(1)/c)-3*pi/2)&
                                    *sin((k_z)*(2*pi*x(3)/c))*(k_z)*(2*pi/c)
end function degg_bottom
real pure function dotegg_bottom(x)
  real,intent(in) :: x(3)
  dotegg_bottom = 0
end function dotegg_bottom
end program swimming_plate

