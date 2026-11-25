from typing import Optional, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database.session import SessionLocal, get_db
from app.core.config import settings
from app.core.security import decode_token
from app.models.user import User
from app.models.membership import Membership
from app.models.hostel import Hostel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        if payload is None:
            raise credentials_exception
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
    except (JWTError, ValueError, TypeError):
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled",
        )
    return user


def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db_session),
) -> Optional[User]:
    if not token:
        return None
    try:
        return get_current_user(token, db)
    except HTTPException:
        return None


def require_role(allowed_roles: List[str]):
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation requires one of roles: {', '.join(allowed_roles)}",
            )
        return current_user
    return role_checker


def require_super_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super admin access required",
        )
    return current_user


def require_hostel_member(
    hostel_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
) -> User:
    """Verify that the current user belongs to the specified hostel."""
    membership = (
        db.query(Membership)
        .filter(
            Membership.user_id == current_user.id,
            Membership.hostel_id == hostel_id,
            Membership.is_active == True,
        )
        .first()
    )
    if not membership:
        if current_user.role == "super_admin":
            return current_user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this hostel",
        )
    return current_user


def require_hostel_role(
    hostel_id: int,
    allowed_roles: List[str],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
) -> User:
    """Verify user membership and role in a hostel."""
    if current_user.role == "super_admin":
        return current_user

    membership = (
        db.query(Membership)
        .filter(
            Membership.user_id == current_user.id,
            Membership.hostel_id == hostel_id,
            Membership.is_active == True,
        )
        .first()
    )
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this hostel",
        )
    if membership.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Operation requires role: {', '.join(allowed_roles)} in this hostel",
        )
    return current_user


def get_user_hostels(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
) -> List[Membership]:
    """Get all active hostel memberships for a user."""
    if current_user.role == "super_admin":
        return db.query(Membership).filter(Membership.is_active == True).all()
    return (
        db.query(Membership)
        .filter(Membership.user_id == current_user.id, Membership.is_active == True)
        .all()
    )


def get_hostel_or_404(
    hostel_id: int,
    db: Session = Depends(get_db_session),
) -> Hostel:
    hostel = db.query(Hostel).filter(Hostel.id == hostel_id).first()
    if not hostel:
        raise HTTPException(status_code=404, detail="Hostel not found")
    return hostel