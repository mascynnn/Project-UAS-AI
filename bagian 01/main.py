import csv
from math import log2
import pprint

# Load dataset dari CSV
def load_dataset(filename):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        data = list(csv.DictReader(csvfile))
        hasil = []
        for row in data:
            try:
                study_hours = float(row['Study_Hours_per_Week'])
                midterm = float(row['Midterm_Score'])
                final = float(row['Final_Score'])
                total = float(row['Total_Score'])
                label = 'Pass' if total >= 60 else 'Fail'

                hasil.append({
                    'Study_Hours': study_hours,
                    'Midterm_Score': midterm,
                    'Final_Score': final,
                    'Result': label
                })
            except:
                continue
        return hasil

# Hitung entropy
def entropy(data):
    total = len(data)
    if total == 0:
        return 0
    label_count = {}
    for row in data:
        label = row['Result']
        label_count[label] = label_count.get(label, 0) + 1
    return -sum((c / total) * log2(c / total) for c in label_count.values())

# Split data berdasarkan threshold
def split_data(data, attr, threshold):
    kiri = [row for row in data if row[attr] <= threshold]
    kanan = [row for row in data if row[attr] > threshold]
    return kiri, kanan

# Hitung information gain
def information_gain(data, attr, threshold):
    kiri, kanan = split_data(data, attr, threshold)
    p = len(kiri) / len(data)
    return entropy(data) - (p * entropy(kiri) + (1 - p) * entropy(kanan))

# Bangun pohon keputusan (ID3)
def build_tree(data, attributes):
    labels = [row['Result'] for row in data]
    if labels.count(labels[0]) == len(labels):
        return labels[0]
    if not attributes:
        return max(set(labels), key=labels.count)

    best_attr = None
    best_thresh = None
    best_gain = -1

    for attr in attributes:
        values = sorted(set(row[attr] for row in data))
        thresholds = [(values[i] + values[i+1]) / 2 for i in range(len(values)-1)]
        for t in thresholds:
            gain = information_gain(data, attr, t)
            if gain > best_gain:
                best_attr = attr
                best_thresh = t
                best_gain = gain

    if best_gain == 0:
        return max(set(labels), key=labels.count)

    kiri, kanan = split_data(data, best_attr, best_thresh)
    remaining = [a for a in attributes if a != best_attr]

    return {
        'attribute': best_attr,
        'threshold': best_thresh,
        'left': build_tree(kiri, remaining),
        'right': build_tree(kanan, remaining)
    }

# Prediksi label berdasarkan pohon
def predict(tree, sample):
    if isinstance(tree, str):
        return tree
    if sample[tree['attribute']] <= tree['threshold']:
        return predict(tree['left'], sample)
    else:
        return predict(tree['right'], sample)

# Evaluasi akurasi model
def evaluate(tree, data):
    benar = sum(1 for row in data if predict(tree, row) == row['Result'])
    return benar / len(data)

# Main program
if __name__ == "__main__":
    dataset = load_dataset("D:\Kuliah\Kuliah Semester 4\Kecerdasan Buatan\Project UAS\Bagian 02\dataset\Students Performance Dataset.csv")
    fitur = ['Study_Hours', 'Midterm_Score', 'Final_Score']
    pohon = build_tree(dataset, fitur)

    print("\n📊 Pohon Keputusan (ID3, Tanpa Library):")
    pprint.pprint(pohon)

    akurasi = evaluate(pohon, dataset)
    print(f"\n✅ Akurasi di data training: {akurasi * 100:.2f}%")

    # Contoh prediksi
    sampel = {'Study_Hours': 4, 'Midterm_Score': 55, 'Final_Score': 70}
    hasil = predict(pohon, sampel)
    print(f"\n🔍 Prediksi kelulusan untuk sample {sampel}: {hasil}")
