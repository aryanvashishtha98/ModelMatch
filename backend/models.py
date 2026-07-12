"""
SQLAlchemy ORM Models
"""

from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Float,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy.orm import relationship

from datetime import datetime

from backend.database import Base


class Dataset(Base):

    __tablename__ = "datasets"

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    name = Column(
        String(255),
        nullable=False
    )

    source = Column(
        String(50),
        nullable=False
    )

    meta_features = Column(
        JSONB,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    runs = relationship(
        "Run",
        back_populates="dataset",
        cascade="all, delete"
    )

    recommendations = relationship(
        "Recommendation",
        back_populates="dataset",
        cascade="all, delete"
    )


class Run(Base):

    __tablename__ = "runs"

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    dataset_id = Column(
        BigInteger,
        ForeignKey("datasets.id")
    )

    model_name = Column(
        String(100),
        nullable=False
    )

    hyperparameters = Column(JSONB)

    score = Column(Float)

    metric_type = Column(String(50))

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    dataset = relationship(
        "Dataset",
        back_populates="runs"
    )


class Recommendation(Base):

    __tablename__ = "recommendations"

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    dataset_id = Column(
        BigInteger,
        ForeignKey("datasets.id")
    )

    ranked_shortlist = Column(JSONB)

    reasoning = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    dataset = relationship(
        "Dataset",
        back_populates="recommendations"
    )