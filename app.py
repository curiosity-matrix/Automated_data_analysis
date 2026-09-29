from fastapi import FastAPI
import pandas as pd

app = FastAPI()


@app.get("/")
def home():
    return {"status": "FastAPI is running!"}


@app.post("/")
def receive_data(payload: dict):

    # n8n se data lena
    data = payload["data"]

    # data ko DataFrame mein convert karna
    df = pd.DataFrame(data)

    # numeric columns ko number mein convert karna
    for col in df.columns:

        converted = pd.to_numeric(df[col], errors="coerce")

        if converted.notna().sum() == df[col].notna().sum():
            df[col] = converted

    # ---------------- BASIC INFORMATION ----------------

    rows = len(df)

    columns = len(df.columns)

    column_names = list(df.columns)

    # data types
    data_types = df.dtypes.astype(str).to_dict()

    # missing values
    missing_values = df.isnull().sum().to_dict()

    # duplicate rows
    duplicate_rows = int(df.duplicated().sum())

    # ---------------- COLUMN TYPES ----------------

    numerical_columns = list(
        df.select_dtypes(include="number").columns
    )

    categorical_columns = list(
        df.select_dtypes(exclude="number").columns
    )

    # ---------------- NUMERICAL SUMMARY ----------------

    if len(numerical_columns) > 0:

        numerical_summary = (
            df[numerical_columns]
            .describe()
            .round(2)
            .to_dict()
        )

    else:

        numerical_summary = {}

    # ---------------- UNIQUE VALUES ----------------

    unique_values = {}

    for col in categorical_columns:

        unique_values[col] = int(df[col].nunique())

    # ---------------- GRADE DISTRIBUTION ----------------

    grade_distribution = {}

    if "Grade" in df.columns:

        grade_distribution = (
            df["Grade"]
            .value_counts()
            .to_dict()
        )

    # ---------------- AVERAGE SCORES ----------------

    average_scores = {}

    score_columns = [
        "Math_Score",
        "Science_Score",
        "Language_Score",
        "History_Score",
        "Average_Score"
    ]

    existing_score_columns = []

    for col in score_columns:

        if col in df.columns:
            existing_score_columns.append(col)

    if len(existing_score_columns) > 0:

        average_scores = (
            df[existing_score_columns]
            .mean()
            .round(2)
            .to_dict()
        )

    # ==================================================
    # ANALYSIS
    # ==================================================

    # Study hours vs average score

    study_score = {}

    if "Study_Hours_Per_Day" in df.columns and "Average_Score" in df.columns:

        study_score = (
            df.groupby("Study_Hours_Per_Day")["Average_Score"]
            .mean()
            .round(2)
            .to_dict()
        )

    # Attendance vs average score

    attendance_score = {}

    if "Attendance_Rate" in df.columns and "Average_Score" in df.columns:

        attendance_score = (
            df.groupby("Attendance_Rate")["Average_Score"]
            .mean()
            .round(2)
            .to_dict()
        )

    # Stress vs average score

    stress_score = {}

    if "Stress_Level" in df.columns and "Average_Score" in df.columns:

        stress_score = (
            df.groupby("Stress_Level")["Average_Score"]
            .mean()
            .round(2)
            .to_dict()
        )

    # Major vs average score

    major_score = {}

    if "Major" in df.columns and "Average_Score" in df.columns:

        major_score = (
            df.groupby("Major")["Average_Score"]
            .mean()
            .round(2)
            .to_dict()
        )

    # Grade vs average score

    grade_score = {}

    if "Grade" in df.columns and "Average_Score" in df.columns:

        grade_score = (
            df.groupby("Grade")["Average_Score"]
            .mean()
            .round(2)
            .to_dict()
        )

    # ==================================================
    # CORRELATION
    # ==================================================

    correlations = {}

    if "Average_Score" in df.columns:

        correlation_columns = [
            "Study_Hours_Per_Day",
            "Attendance_Rate",
            "Stress_Level",
            "Sleep_Hours_Per_Day",
            "Age"
        ]

        for col in correlation_columns:

            if col in df.columns:

                correlation = df[col].corr(df["Average_Score"])

                correlations[col] = round(correlation, 2)

    # ==================================================
    # RETURN RESULT
    # ==================================================

    return {

        "rows": rows,

        "columns": columns,

        "column_names": column_names,

        "data_types": data_types,

        "missing_values": missing_values,

        "duplicate_rows": duplicate_rows,

        "numerical_columns": numerical_columns,

        "categorical_columns": categorical_columns,

        "numerical_summary": numerical_summary,

        "unique_values": unique_values,

        "grade_distribution": grade_distribution,

        "average_scores": average_scores,

        "study_score": study_score,

        "attendance_score": attendance_score,

        "stress_score": stress_score,

        "major_score": major_score,

        "grade_score": grade_score,

        "correlations": correlations
    }