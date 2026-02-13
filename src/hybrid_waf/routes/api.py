from flask import Blueprint, request, jsonify
import os
import csv
import json
import torch
import torch.nn as nn
import torch.optim as optim
from datetime import datetime
import numpy as np

api_bp = Blueprint('api', __name__)

# Data storage
DATA_FILE = 'training_data.json'
MODEL_INFO_FILE = 'model_info.json'

def load_training_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'samples': []}

def save_training_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def load_model_info():
    if os.path.exists(MODEL_INFO_FILE):
        with open(MODEL_INFO_FILE, 'r') as f:
            return json.load(f)
    return {'status': 'Not trained', 'sample_count': 0, 'last_trained': 'Never'}

def save_model_info(info):
    with open(MODEL_INFO_FILE, 'w') as f:
        json.dump(info, f)

@api_bp.route('/api/upload_data', methods=['POST'])
def upload_data():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        # Read CSV
        content = file.read().decode('utf-8').splitlines()
        reader = csv.reader(content)
        
        data = load_training_data()
        count = 0
        
        for row in reader:
            if len(row) >= 2:
                data['samples'].append({
                    'request': row[0],
                    'label': int(row[1])
                })
                count += 1
        
        save_training_data(data)
        
        info = load_model_info()
        info['sample_count'] = len(data['samples'])
        save_model_info(info)
        
        return jsonify({'success': True, 'message': f'Uploaded {count} samples successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/api/add_sample', methods=['POST'])
def add_sample():
    try:
        req_data = request.json
        request_str = req_data.get('request', '')
        label = req_data.get('label', 0)
        
        if not request_str:
            return jsonify({'success': False, 'error': 'Request string is required'})
        
        data = load_training_data()
        data['samples'].append({
            'request': request_str,
            'label': label
        })
        save_training_data(data)
        
        info = load_model_info()
        info['sample_count'] = len(data['samples'])
        save_model_info(info)
        
        return jsonify({'success': True, 'message': 'Sample added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/api/train_model', methods=['POST'])
def train_model():
    try:
        params = request.json
        epochs = params.get('epochs', 20)
        batch_size = params.get('batch_size', 32)
        learning_rate = params.get('learning_rate', 0.001)
        
        # Load training data
        data = load_training_data()
        samples = data.get('samples', [])
        
        if len(samples) < 10:
            return jsonify({'success': False, 'error': 'Need at least 10 samples to train'})
        
        # Prepare data
        X = [s['request'] for s in samples]
        y = [s['label'] for s in samples]
        
        # Text to sequence
        def text_to_sequence(text, max_len=500):
            seq = [min(ord(c), 127) for c in text[:max_len]]
            seq += [0] * (max_len - len(seq))
            return seq
        
        X_seq = torch.tensor([text_to_sequence(x) for x in X], dtype=torch.long)
        y_tensor = torch.tensor(y, dtype=torch.float32).unsqueeze(1)
        
        # Define model
        class CharCNN(nn.Module):
            def __init__(self):
                super(CharCNN, self).__init__()
                self.embedding = nn.Embedding(128, 128)
                self.conv1 = nn.Conv1d(128, 256, kernel_size=7, padding=3)
                self.pool1 = nn.MaxPool1d(3)
                self.conv2 = nn.Conv1d(256, 256, kernel_size=7, padding=3)
                self.global_pool = nn.AdaptiveMaxPool1d(1)
                self.fc1 = nn.Linear(256, 128)
                self.dropout = nn.Dropout(0.5)
                self.fc2 = nn.Linear(128, 1)
            
            def forward(self, x):
                x = self.embedding(x)
                x = x.transpose(1, 2)
                x = torch.relu(self.conv1(x))
                x = self.pool1(x)
                x = torch.relu(self.conv2(x))
                x = self.global_pool(x).squeeze(2)
                x = torch.relu(self.fc1(x))
                x = self.dropout(x)
                x = torch.sigmoid(self.fc2(x))
                return x
        
        model = CharCNN()
        criterion = nn.BCELoss()
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)
        
        # Training
        model.train()
        log_lines = []
        final_loss = 0
        final_acc = 0
        
        for epoch in range(epochs):
            optimizer.zero_grad()
            outputs = model(X_seq)
            loss = criterion(outputs, y_tensor)
            loss.backward()
            optimizer.step()
            
            # Calculate accuracy
            predictions = (outputs > 0.5).float()
            accuracy = (predictions == y_tensor).float().mean().item() * 100
            
            final_loss = loss.item()
            final_acc = accuracy
            
            if epoch % 5 == 0:
                log_lines.append(f"Epoch {epoch+1}/{epochs} - Loss: {loss.item():.4f}, Accuracy: {accuracy:.2f}%")
        
        # Save model
        torch.save(model.state_dict(), 'cnn_model.pth')
        
        # Update model info
        info = {
            'status': 'Trained',
            'sample_count': len(samples),
            'last_trained': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'epochs': epochs,
            'accuracy': f"{final_acc:.2f}"
        }
        save_model_info(info)
        
        return jsonify({
            'success': True,
            'accuracy': f"{final_acc:.2f}",
            'loss': f"{final_loss:.4f}",
            'log': '\n'.join(log_lines)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/api/test_model', methods=['POST'])
def test_model():
    try:
        from src.hybrid_waf.utils.signature_checker import check_signature
        from src.hybrid_waf.utils.cnn_checker import check_cnn
        
        req_data = request.json
        request_str = req_data.get('request', '')
        
        if not request_str:
            return jsonify({'success': False, 'error': 'Request string is required'})
        
        # Check signature first
        sig_result = check_signature(request_str)
        if sig_result['is_malicious']:
            return jsonify({
                'success': True,
                'prediction': 1,
                'confidence': 1.0,
                'method': f"Signature ({sig_result['attack_type']})"
            })
        
        # Check CNN
        cnn_result = check_cnn(request_str)
        return jsonify({
            'success': True,
            'prediction': 1 if cnn_result['is_malicious'] else 0,
            'confidence': cnn_result['confidence'],
            'method': 'CNN'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_bp.route('/api/model_info', methods=['GET'])
def model_info():
    try:
        info = load_model_info()
        return jsonify(info)
    except Exception as e:
        return jsonify({'status': 'Error', 'sample_count': 0, 'last_trained': 'Never'})
