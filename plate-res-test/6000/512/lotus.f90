program swimming_plate
  !
    use bodyMod,    only: body
    use fluidMod,   only: fluid
    use mympiMod,   only: init_mympi,mympi_end,mympi_rank
    use gridMod,    only: xg,composite
    use imageMod,   only: display
    use geom_shape
    implicit none
  !
  ! -- Physical parameters
    real,parameter     :: Re = 5000
  !
    real,parameter     :: L=512, nu=L/Re
    real, parameter    :: finish=6
    integer            :: b(3) = [8,8,1]
  !
  ! -- Hyperparameters
    real, parameter    :: thicc=0.03*L
    real, parameter    :: A = 0.1*L, St_d = 0.3, k_x=20.5, k_z=20.0, h_roughness=0.0
    real, parameter    :: a_coeff = 0.28/2, &
                          b_coeff = -0.13/2, &
                          c_coeff = 0.05/2, &
                          k_coeff = 1., &
                          f = St_d/(2*A)
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
      n = composite(L*m,prnt=root)
      call xg(1)%stretch(n(1), -2.0*L, -.5*L, 2.5*L, 7.0*L,  h_min=4., h_max=10., prnt=root)
      call xg(2)%stretch(n(2), -2.0*L, -0.9*L, 0.9*L, 2.0*L, h_min=2., prnt=root)
      if(ndims==3) xg(3)%h = 4.
    !
    ! -- Call the geometry and kinematics
      
      geom = plate(L, thicc).map.init_warp(2,h,doth,dh)
    !
    ! -- Initialise fluid
      call flow%init(n/b,geom,V=[1.,0.,0.],nu=nu,exit=.true.)
      ! flow%time = 0
    !
      if(root) print *,'Starting time update loop'
      if(root) print *,'-----------------------------------'
    !
      time_loop: do while (flow%time<finish/f.and..not.there)
        t = flow%time
        dt = flow%dt
        call geom%update(t+dt) ! update geom
        call flow%update(geom)
  
        write(9,'(f10.4,f8.4,4e16.8,4e16.8,4e16.8,4e16.8,4e16.8,4e16.8)')&
              t*f,dt,pforce,ppower,vforce,vforce1,vforce2,&
              enstrophy_body,enstrophy_wake,tke_body,tke_wake,enstrophy,tke
  
        pforce = 2.*geom%pforce(flow%pressure)/(L*n(3)*xg(3)%h)
        ppower = 2.*geom%ppower(flow%pressure)/(L*n(3)*xg(3)%h)
        vforce = 2.*nu*geom%vforce(flow%velocity)/(L*n(3)*xg(3)%h)
        vforce1 = 2.*nu*geom%vforce_f(flow%velocity)/(L*n(3)*xg(3)%h)
        vforce2 = 2.*nu*geom%vforce_s(flow%velocity)/(L*n(3)*xg(3)%h)
        enstrophy_body = flow%velocity%enstrophy(lcorn=L*[-0.25,-0.5,0.],ucorn=L*[2.0,0.5,0.125])
        enstrophy_wake = flow%velocity%enstrophy(lcorn=L*[1.1,-0.5,0.],ucorn=L*[2.1,0.5,0.125])
        enstrophy = flow%velocity%enstrophy()
        tke_body = flow%velocity%tke(lcorn=L*[-0.25,-0.5,0.],ucorn=L*[2.0,0.5,0.125])
        tke_wake = flow%velocity%tke(lcorn=L*[1.1,-0.5,0.],ucorn=L*[2.1,0.5,0.125])
        tke = flow%velocity%tke()
  
        if((mod(t,1./f)<dt).and.(root)) print "('Time:',f15.3)",&
        t*f
  
        inquire(file='.kill', exist=there)
        if(there) exit time_loop
        ! if((t>(finish-1)/f).and.(mod(t,0.1/f)<dt)) call flow%write(geom, write_vtr=.false.)
      end do time_loop
      
      if(root) print *,'Loop complete: writing restart files and exiting'
      ! call flow%write(geom)
      if(root) print *,'-----------------------------------'
    call mympi_end
  contains
  !
  type(set) function plate(length, thickness) result(geom)
    real,intent(in) :: length, thickness
    geom = upper(length, thickness).and.lower(length, thickness) &
    .and.plane([1.,-0.,0.],[length,0.,0.]) & ! end cap
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
          - amp(x(1))*cos(arg(x(1)))*2*pi*k_coeff/L
  end function dh
  real pure function arg(x)
    real,intent(in) :: x
    real :: xp
    xp = min(max(x/L,0.),1.)
    arg = (2*pi*(f*flow%time - k_coeff*xp))
  end function arg
  real pure function amp(x)
    real,intent(in) :: x
    real :: xp
    xp = min(max(x/L,0.),1.)
    amp = A*(((a_coeff*(xp**2))+(b_coeff*(xp))+(c_coeff))/(a_coeff+b_coeff+c_coeff))
  end function amp
  real pure function damp(x)
    real,intent(in) :: x
    real :: xp
    xp = min(max(x/L,0.),1.)
    damp = A*(b_coeff+2.*(a_coeff*xp))/(L*(a_coeff+b_coeff+c_coeff))
  end function damp
  !
  ! -- Egg carton roughness distribution
  real pure function egg_top(x)
    real,intent(in) :: x(3)
    egg_top = (h_roughness*L)*sin((k_x)*(2*pi*x(1)/L)-pi/2)&
                              *cos((k_z)*(2*pi*x(3)/L))
  end function egg_top
  pure function degg_top(x)
    real,intent(in) :: x(3)
    real            :: degg_top(3)
    degg_top = 0
    degg_top(1) = (h_roughness*L)*cos((k_x)*(2*pi*x(1)/L)-pi/2)&
                                  *sin((k_z)*(2*pi*x(3)/L))*(k_x)*(2*pi/L)
    degg_top(3) = -(h_roughness*L)*cos((k_x)*(2*pi*x(1)/L)-pi/2)&
                                  *sin((k_z)*(2*pi*x(3)/L))*(k_z)*(2*pi/L)
  end function degg_top
  real pure function dotegg_top(x)
    real,intent(in) :: x(3)
    dotegg_top = 0
  end function dotegg_top
  !
  real pure function egg_bottom(x)
    real,intent(in) :: x(3)
    egg_bottom = (h_roughness*L)*sin((k_x)*(2*pi*x(1)/L)-3*pi/2)&
                                *cos((k_z)*(2*pi*x(3)/L))
  end function egg_bottom
  pure function degg_bottom(x)
    real,intent(in) :: x(3)
    real            :: degg_bottom(3)
    degg_bottom = 0
    degg_bottom(1) = (h_roughness*L)*cos((k_x)*(2*pi*x(1)/L)-3*pi/2)&
                                      *sin((k_z)*(2*pi*x(3)/L))*(k_x)*(2*pi/L)
    degg_bottom(3) = -(h_roughness*L)*cos((k_x)*(2*pi*x(1)/L)-3*pi/2)&
                                      *sin((k_z)*(2*pi*x(3)/L))*(k_z)*(2*pi/L)
  end function degg_bottom
  real pure function dotegg_bottom(x)
    real,intent(in) :: x(3)
    dotegg_bottom = 0
  end function dotegg_bottom
end program swimming_plate  