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
  real,parameter     :: Re = 12000
!
    real,parameter     :: c=1024, nu=c/Re
  real, parameter    :: finish=7
  integer            :: b(3) = [8,8,1]
!
! -- Hyperparameters
  real, parameter    :: thicc=0.03*c
  real, parameter    :: A = 0.1*c, St_d = 0.3, k_x=0., k_z=4.0, h_roughness=0.0
  real, parameter    :: a_coeff = 0.28, &
                        b_coeff = 0.13, &
                        c_coeff = 0.05, &
                        k_coeff = 0.94, &
                        f = St_d/(2.*A)
!
! -- Dimensions
  integer            :: n(3), ndims=2
!
! -- Setup solver
  logical            :: there = .false., root, p(3) = [.FALSE.,.FALSE.,.TRUE.]
  real               :: m(3), z
  type(fluid)        :: flow
  type(body)         :: geom
  ! type(avrgField)    :: avrg
!
!
! -- Outputs
  real            :: dt, t, pforce(3),vforce(3),vforce1(3),vforce2(3),ppower
  real            :: enstrophy_body,enstrophy_wake,enstrophy,tke_body,tke_wake,tke
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
    z = 0.03125
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
    call flow%update(geom)              ! update N-S

    pforce = 2.*geom%pforce(flow%pressure)/(c*n(3)*xg(3)%h)
    ppower = 2.*geom%ppower(flow%pressure)/(c*n(3)*xg(3)%h)
    vforce = 2.*nu*geom%vforce(flow%velocity)/(c*n(3)*xg(3)%h)
    vforce1 = 2.*nu*geom%vforce_f(flow%velocity)/(c*n(3)*xg(3)%h)
    vforce2 = 2.*nu*geom%vforce_s(flow%velocity)/(c*n(3)*xg(3)%h)
    enstrophy_body = flow%velocity%enstrophy(lcorn=c*[-0.25,-0.5,0.],ucorn=c*[2.0,0.5,0.125])
    enstrophy_wake = flow%velocity%enstrophy(lcorn=c*[1.1,-0.5,0.],ucorn=c*[2.1,0.5,0.125])
    enstrophy = flow%velocity%enstrophy()
    tke_body = flow%velocity%tke(lcorn=c*[-0.25,-0.5,0.],ucorn=c*[2.0,0.5,0.125])
    tke_wake = flow%velocity%tke(lcorn=c*[1.1,-0.5,0.],ucorn=c*[2.1,0.5,0.125])
    tke = flow%velocity%tke()
    
    write(9,'(f10.4,f8.4,4e16.8,4e16.8,4e16.8,4e16.8,4e16.8,4e16.8)')&
          t*f,flow%dt,pforce,ppower,vforce,vforce1,vforce2,&
          enstrophy_body,enstrophy_wake,tke_body,tke_wake,enstrophy,tke

    if((mod(t,1./f)<flow%dt).and.(root)) print "('Time:',f15.3)",t*f

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
  real :: xp
  xp = min(max(x/c,0.),1.)
  amp = A*(((a_coeff*(xp**2))+(b_coeff*(xp))+(c_coeff))/(a_coeff+b_coeff+c_coeff))
end function amp
real pure function damp(x)
  real,intent(in) :: x
  real :: xp
  xp = min(max(x/c,0.),1.)
  damp = A*(b_coeff+2.*(a_coeff*xp))/(c*(a_coeff+b_coeff+c_coeff))
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