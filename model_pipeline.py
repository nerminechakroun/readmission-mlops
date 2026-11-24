import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split


def prepare_data(data_path):
    """
    Charge et prétraite les données.
    """

    df = pd.read_csv(data_path)

    # Création de la variable cible
    df["readmitted_binary"] = df["readmitted"].apply(lambda x: 1 if x == "<30" else 0)

    # Suppression des colonnes inutiles
    columns_to_remove = [
        "encounter_id",
        "patient_nbr",
        "weight",
        "payer_code",
        "medical_specialty",
    ]

    df_cleaned = df.drop(columns=columns_to_remove, errors="ignore")

    # Gestion des valeurs manquantes
    df_cleaned = df_cleaned.replace("?", np.nan)

    for col in df_cleaned.columns:
        if df_cleaned[col].isnull().sum() > 0:
            if df_cleaned[col].dtype == "object":
                df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].mode()[0])
            else:
                df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].median())

    # Encodage des variables catégorielles
    categorical_cols = df_cleaned.select_dtypes(include=["object"]).columns.tolist()

    categorical_cols = [
        col
        for col in categorical_cols
        if col not in ["readmitted", "readmitted_binary"]
    ]

    for col in categorical_cols:
        le = LabelEncoder()
        df_cleaned[col] = le.fit_transform(df_cleaned[col].astype(str))

    # Séparation X / y
    X = df_cleaned.drop(["readmitted", "readmitted_binary"], axis=1)

    y = df_cleaned["readmitted_binary"]

    # Train / Test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Standardisation
    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print("\n=== DATA PREPARATION ===")
    print("X_train shape :", X_train_scaled.shape)
    print("X_test shape  :", X_test_scaled.shape)
    print("y_train shape :", y_train.shape)
    print("y_test shape  :", y_test.shape)
    print("Préparation des données terminée.")
    return (X_train_scaled, X_test_scaled, y_train, y_test, scaler)


def train_model(X_train, y_train):
    from sklearn.ensemble import RandomForestClassifier

    model = RandomForestClassifier(n_estimators=100, random_state=42)

    model.fit(X_train, y_train)
    print("\n✅ ENTRAÎNEMENT DU MODÈLE TERMINÉ AVEC SUCCÈS !")
    return model


def evaluate_model(model, X_test, y_test):
    from sklearn.metrics import accuracy_score, classification_report

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    print("Accuracy :", accuracy)
    print("\nClassification Report :")
    print(classification_report(y_test, y_pred))

    return accuracy


def save_model(model, path):
    import joblib

    joblib.dump(model, path)
    print("Modèle sauvegardé :", path)


def load_model(path):
    import joblib

    model = joblib.load(path)
    print("Modèle chargé :", path)

    return model
