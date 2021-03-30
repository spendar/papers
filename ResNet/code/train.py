import torch
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision import transforms
from torch import nn, optim
from resnet import resnet18

batch_size = 32


# 准备数据集
train_data = datasets.CIFAR10(root='', train = True, transform = transforms.Compose([
	transforms.Resize((32,32)),
	transforms.ToTensor(),
	transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
	]),download=True)
trainloader = DataLoader(train_data,batch_size=batch_size, shuffle=True)

test_data = datasets.CIFAR10(root='cifar/', train=False, transform=transforms.Compose([
        transforms.Resize((32, 32)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ]),download=True)
testloader = DataLoader(test_data,batch_size=batch_size,shuffle=True)

# 模型准备
device = torch.device('cuda')
model = resnet18().to(device)
criterion = nn.CrossEntropyLoss().to(device)
optimizer = optim.Adam(model.parameters(), lr=0.001)
print(model)

for epoch in range(300):
	model.train()
	for batch_id, (x, label) in enumerate(trainloader):
		x, label = x.to(device), label.to(device)
		res = model(x)
		loss = criterion(res, label)
		optimizer.zero_grad()
		loss.backward()
		optimizer.step()
	print(epoch, 'loss', loss.item())

	model.eval()
	with torch.no_gard():
		total_correct = 0
		total_num = 0
		for x, label in testloader:
			x, label = x.to(device), label.to(device)
			res = model(x)
			pred = res.argmaxn(dim=1)
			correct = torch.eq(pred,label).float().sum().item()
			total_correct += correct
			total_num += x.size(0)
		acc = total_correct / total_num
		print(epoch, 'test acc: ', acc)