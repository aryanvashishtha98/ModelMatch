-- =====================================================
-- ModelMatch Database Schema
-- PostgreSQL (Supabase)
-- =====================================================

-- ==========================
-- DATASETS TABLE
-- ==========================

CREATE TABLE datasets (

    id BIGSERIAL PRIMARY KEY,

    name VARCHAR(255) NOT NULL,

    source VARCHAR(50) NOT NULL,

    meta_features JSONB NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- ==========================
-- RUNS TABLE
-- ==========================

CREATE TABLE runs (

    id BIGSERIAL PRIMARY KEY,

    dataset_id BIGINT NOT NULL,

    model_name VARCHAR(150) NOT NULL,

    hyperparameters JSONB,

    score DOUBLE PRECISION NOT NULL,

    metric_type VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_dataset

        FOREIGN KEY(dataset_id)

        REFERENCES datasets(id)

        ON DELETE CASCADE

);

-- ==========================
-- RECOMMENDATIONS TABLE
-- ==========================

CREATE TABLE recommendations (

    id BIGSERIAL PRIMARY KEY,

    dataset_id BIGINT NOT NULL,

    ranked_shortlist JSONB NOT NULL,

    reasoning TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_recommendation_dataset

        FOREIGN KEY(dataset_id)

        REFERENCES datasets(id)

        ON DELETE CASCADE

);

-- ==========================
-- INDEXES
-- ==========================

CREATE INDEX idx_dataset_name
ON datasets(name);

CREATE INDEX idx_runs_dataset
ON runs(dataset_id);

CREATE INDEX idx_runs_model
ON runs(model_name);

CREATE INDEX idx_recommendation_dataset
ON recommendations(dataset_id);

CREATE INDEX idx_dataset_meta
ON datasets
USING GIN(meta_features);

CREATE INDEX idx_runs_score
ON runs(score DESC);

-- ==========================
-- SAMPLE QUERY
-- ==========================

-- Get all model runs for a dataset

SELECT

d.name,

r.model_name,

r.score,

r.metric_type,

r.created_at

FROM datasets d

JOIN runs r

ON d.id = r.dataset_id;

-- ==========================
-- Recommendation History
-- ==========================

SELECT

d.name,

rec.reasoning,

rec.created_at

FROM recommendations rec

JOIN datasets d

ON rec.dataset_id=d.id;