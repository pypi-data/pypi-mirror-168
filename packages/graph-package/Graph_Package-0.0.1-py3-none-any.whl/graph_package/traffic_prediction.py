import matplotlib.pyplot as plt
from torch_geometric_temporal.signal import temporal_signal_split
import seaborn as sns
import torch
from IPython.display import clear_output
import numpy as np
from torch_geometric_temporal.dataset import METRLADatasetLoader, ChickenpoxDatasetLoader
import torch.nn.functional as F
from torch_geometric_temporal.nn.recurrent import A3TGCN


loader = METRLADatasetLoader()
dataset = loader.get_dataset(num_timesteps_in=12, num_timesteps_out=12)
labs = np.asarray([label[loader.sensor][loader.timestep].cpu().numpy()
                  for label in loader.labels])
# Show first sample
next(iter(dataset))
d = ChickenpoxDatasetLoader().get_dataset(lags=4)
next(iter(d))
# Visualize traffic over time
sensor_number = 1
hours = 24
sensor_labels = [bucket.y[sensor_number][0].item()
                 for bucket in list(dataset)[:hours]]
sns.lineplot(data=sensor_labels)
train_dataset, test_dataset = temporal_signal_split(dataset, train_ratio=0.8)


class TemporalGNN(torch.nn.Module):
    def __init__(self, node_features, periods):
        super(TemporalGNN, self).__init__()
        # Attention Temporal Graph Convolutional Cell
        self.tgnn = A3TGCN(in_channels=node_features,
                           out_channels=32,
                           periods=periods)
        # Equals single-shot prediction
        self.linear = torch.nn.Linear(32, periods)

    def forward(self, x, edge_index):
        """
        x = Node features for T time steps
        edge_index = Graph edge indices
        """
        h = self.tgnn(x, edge_index)
        h = F.relu(h)
        h = self.linear(h)
        return h


TemporalGNN(node_features=2, periods=12)

# GPU support
device = torch.device('cpu')  # cuda
subset = 2000

# Create model and optimizers
model = TemporalGNN(node_features=2, periods=12).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
model.train()

print("Running training...")
for epoch in range(6):
    loss = 0
    step = 0
    for snapshot in train_dataset:
        snapshot = snapshot.to(device)
        # Get model predictions
        y_hat = model(snapshot.x, snapshot.edge_index)
        # Mean squared error
        loss = loss + torch.mean((y_hat-snapshot.y)**2)
        step += 1
        if step > subset:
            break

    loss = loss / (step + 1)
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
model.eval()
loss = 0
step = 0
horizon = 288

# Store for analysis
predictions = []
labels = []

for snapshot in test_dataset:
    snapshot = snapshot.to(device)
    # Get predictions
    y_hat = model(snapshot.x, snapshot.edge_index)
    # Mean squared error
    loss = loss + torch.mean((y_hat-snapshot.y)**2)
    # Store for analysis below
    labels.append(snapshot.y)
    predictions.append(y_hat)
    step += 1
    if step > horizon:
        break

loss = loss / (step+1)
loss = loss.item()

sensor = 123
timestep = 11
preds = np.asarray([pred[sensor][timestep].detach().cpu().numpy()
                   for pred in predictions])
labs = np.asarray([label[sensor][timestep].cpu().numpy() for label in labels])

plt.figure(figsize=(20, 5))
sns.lineplot(data=preds, label="pred")
sns.lineplot(data=labs, label="true")
