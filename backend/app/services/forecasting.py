import numpy as np
import torch
from torch import nn


class LSTMForecaster(nn.Module):
    def __init__(self, input_size: int = 1, hidden_size: int = 32):
        super().__init__()

        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            batch_first=True,
        )

        self.output = nn.Linear(hidden_size, 1)

    def forward(self, x):
        output, _ = self.lstm(x)
        return self.output(output[:, -1, :])


def create_sequences(
    values: list[float],
    sequence_length: int = 7,
) -> tuple[np.ndarray, np.ndarray]:

    if len(values) <= sequence_length:
        raise ValueError(
            "Not enough data to create forecasting sequences."
        )

    x = []
    y = []

    for i in range(len(values) - sequence_length):
        x.append(values[i:i + sequence_length])
        y.append(values[i + sequence_length])

    return np.array(x), np.array(y)


def train_lstm(
    values: list[float],
    sequence_length: int = 7,
    epochs: int = 100,
) -> LSTMForecaster:

    x, y = create_sequences(values, sequence_length)

    x_tensor = torch.tensor(
        x,
        dtype=torch.float32,
    ).unsqueeze(-1)

    y_tensor = torch.tensor(
        y,
        dtype=torch.float32,
    ).unsqueeze(-1)

    model = LSTMForecaster()

    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=0.01,
    )

    model.train()

    for _ in range(epochs):
        optimizer.zero_grad()

        predictions = model(x_tensor)
        loss = criterion(predictions, y_tensor)

        loss.backward()
        optimizer.step()

    return model


def forecast_next_days(
    model: LSTMForecaster,
    values: list[float],
    days: int = 15,
    sequence_length: int = 7,
) -> list[float]:

    model.eval()

    history = list(values)
    predictions = []

    for _ in range(days):
        sequence = history[-sequence_length:]

        x_tensor = torch.tensor(
            sequence,
            dtype=torch.float32,
        ).reshape(1, sequence_length, 1)

        with torch.no_grad():
            prediction = model(x_tensor).item()

        prediction = max(0.0, prediction)

        predictions.append(prediction)
        history.append(prediction)

    return predictions