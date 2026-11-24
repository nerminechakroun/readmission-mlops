import argparse

from model_pipeline import (
    prepare_data,
    train_model,
    evaluate_model,
    save_model,
    load_model,
)

DATA_PATH = "data/diabetic_data.csv"
MODEL_PATH = "models/readmission_model.joblib"


def prepare():
    return prepare_data(DATA_PATH)


def train():
    X_train, X_test, y_train, y_test, scaler = prepare_data(DATA_PATH)

    model = train_model(X_train, y_train)

    return model


def save():
    X_train, X_test, y_train, y_test, scaler = prepare_data(DATA_PATH)

    model = train_model(X_train, y_train)

    save_model(model, MODEL_PATH)


def load():
    return load_model(MODEL_PATH)


def evaluate():
    X_train, X_test, y_train, y_test, scaler = prepare_data(DATA_PATH)

    model = load_model(MODEL_PATH)

    evaluate_model(model, X_test, y_test)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--train", action="store_true")
    parser.add_argument("--save", action="store_true")
    parser.add_argument("--load", action="store_true")
    parser.add_argument("--evaluate", action="store_true")

    args = parser.parse_args()

    if args.prepare:
        prepare()

    elif args.train:
        train()

    elif args.save:
        save()

    elif args.load:
        load()

    elif args.evaluate:
        evaluate()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
