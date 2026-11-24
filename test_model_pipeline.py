from model_pipeline import train_model, evaluate_model


def test_train_model():
    X_train = [
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 5]
    ]

    y_train = [0, 0, 1, 1]

    model = train_model(X_train, y_train)

    assert model is not None


def test_evaluate_model():
    X_train = [
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 5]
    ]

    y_train = [0, 0, 1, 1]

    model = train_model(X_train, y_train)

    accuracy = evaluate_model(
        model,
        X_train,
        y_train
    )

    assert 0 <= accuracy <= 1
