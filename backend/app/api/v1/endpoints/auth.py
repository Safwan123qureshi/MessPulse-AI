from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.core.security import create_access_token, create_refresh_token, decode_token, verify_password, get_password_hash
from app.models.user import User
from app.models.membership import Membership
from app.models.hostel import Hostel
from app.schemas.user import UserCreate, UserResponse, Token, LoginRequest, TokenData
from app.schemas.membership import UserMembershipResponse
from app.api.deps import get_db_session, get_current_user, require_super_admin

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new user (platform level)."""
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        phone=user_in.phone,
        role=user_in.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(login_in: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return access/refresh tokens."""
    user = db.query(User).filter(User.email == login_in.email).first()
    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=401, detail="Account is disabled")

    user.last_login = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
    db.commit()

    # Get user's hostel memberships
    memberships = (
        db.query(Membership)
        .filter(Membership.user_id == user.id, Membership.is_active == True)
        .all()
    )
    hostel_ids = [m.hostel_id for m in memberships]

    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role, "hostel_ids": hostel_ids}
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
def refresh_token(token_data: TokenData, db: Session = Depends(get_db)):
    """Refresh access token using refresh token."""
    # In production, verify refresh token separately
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    memberships = (
        db.query(Membership)
        .filter(Membership.user_id == user.id, Membership.is_active == True)
        .all()
    )
    hostel_ids = [m.hostel_id for m in memberships]

    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role, "hostel_ids": hostel_ids}
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user profile."""
    return current_user


@router.get("/me/memberships", response_model=list[UserMembershipResponse])
def get_user_memberships(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
):
    """Get current user's hostel memberships."""
    memberships = (
        db.query(Membership)
        .filter(Membership.user_id == current_user.id, Membership.is_active == True)
        .all()
    )
    result = []
    for m in memberships:
        hostel = db.query(Hostel).filter(Hostel.id == m.hostel_id).first()
        result.append(
            UserMembershipResponse(
                id=m.id,
                hostel_id=m.hostel_id,
                hostel_name=hostel.name if hostel else "",
                role=m.role,
                is_active=m.is_active,
            )
        )
    return result


@router.post("/super-admin/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_super_admin(
    user_in: UserCreate,
    current_user: User = Depends(require_super_admin),
    db: Session = Depends(get_db_session),
):
    """Create a super admin (only existing super admin can do this)."""
    user_in.role = "super_admin"
    return register_user(user_in, db)