-- Asumsi menggunakan PostgreSQL
-- Tabel grades (contoh struktur, sesuaikan jika berbeda)
CREATE TABLE IF NOT EXISTS grades (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL,
    course_id VARCHAR(20) NOT NULL,
    grade VARCHAR(2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabel grade_history untuk audit
CREATE TABLE IF NOT EXISTS grade_history (
    id SERIAL PRIMARY KEY,
    grade_id INTEGER NOT NULL REFERENCES grades(id),
    old_value VARCHAR(2),
    new_value VARCHAR(2) NOT NULL,
    changed_by VARCHAR(100),  -- Username atau ID user yang ubah
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reason TEXT
);

-- Trigger function untuk audit
CREATE OR REPLACE FUNCTION audit_grade_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.grade != NEW.grade THEN
        INSERT INTO grade_history (grade_id, old_value, new_value, changed_by, reason)
        VALUES (NEW.id, OLD.grade, NEW.grade, NEW.changed_by, NEW.change_reason);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger pada tabel grades
CREATE TRIGGER grade_update_trigger
    AFTER UPDATE ON grades
    FOR EACH ROW
    EXECUTE FUNCTION audit_grade_changes();

-- View untuk lihat riwayat perubahan per mahasiswa
-- Asumsi ada tabel students dengan id dan name
CREATE TABLE IF NOT EXISTS students (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE VIEW student_grade_history AS
SELECT
    s.id AS student_id,
    s.name AS student_name,
    g.course_id,
    gh.old_value,
    gh.new_value,
    gh.changed_by,
    gh.changed_at,
    gh.reason
FROM
    grade_history gh
JOIN
    grades g ON gh.grade_id = g.id
JOIN
    students s ON g.student_id = s.id
ORDER BY
    s.id, gh.changed_at DESC;