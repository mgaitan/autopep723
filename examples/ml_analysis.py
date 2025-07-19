#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "matplotlib",
#     "pandas",
#     "scikit-learn",
#     "seaborn",
# ]
# ///


import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def generate_sample_data():
    """Generate sample classification dataset."""
    print("Generating sample dataset...")

    # Create synthetic dataset
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_informative=15,
        n_redundant=5,
        n_classes=3,
        random_state=42
    )

    # Convert to DataFrame for easier handling
    feature_names = [f'feature_{i}' for i in range(X.shape[1])]
    df = pd.DataFrame(X, columns=feature_names)
    df['target'] = y

    return df


def explore_data(df):
    """Perform basic data exploration."""
    print("\n=== Data Exploration ===")
    print(f"Dataset shape: {df.shape}")
    print(f"Features: {df.columns.tolist()[:-1]}")
    print(f"Target classes: {sorted(df['target'].unique())}")

    # Basic statistics
    print("\nTarget distribution:")
    print(df['target'].value_counts().sort_index())

    # Check for missing values
    missing_values = df.isnull().sum().sum()
    print(f"Missing values: {missing_values}")

    return df


def visualize_data(df):
    """Create visualizations of the dataset."""
    print("\n=== Creating Visualizations ===")

    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 8)

    # Create subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))

    # Target distribution
    df['target'].value_counts().sort_index().plot(kind='bar', ax=axes[0, 0])
    axes[0, 0].set_title('Target Class Distribution')
    axes[0, 0].set_xlabel('Class')
    axes[0, 0].set_ylabel('Count')

    # Feature correlation heatmap (first 10 features)
    corr_matrix = df.iloc[:, :10].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=axes[0, 1])
    axes[0, 1].set_title('Feature Correlation Matrix (First 10 Features)')

    # Feature distributions
    df.iloc[:, :5].hist(bins=20, ax=axes[1, 0])
    axes[1, 0].set_title('Distribution of First 5 Features')

    # Box plot of features by target
    df_melted = pd.melt(df.iloc[:, :5], id_vars=[], value_vars=df.columns[:5])
    sns.boxplot(data=df_melted, x='variable', y='value', ax=axes[1, 1])
    axes[1, 1].set_title('Feature Distributions')
    axes[1, 1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig('data_exploration.png', dpi=300, bbox_inches='tight')
    print("✓ Saved visualization: data_exploration.png")

    plt.show()


def train_model(df):
    """Train a machine learning model."""
    print("\n=== Training Model ===")

    # Prepare features and target
    X = df.drop('target', axis=1)
    y = df['target']

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Training set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train Random Forest model
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )

    print("Training Random Forest classifier...")
    rf_model.fit(X_train_scaled, y_train)

    # Make predictions
    y_pred = rf_model.predict(X_test_scaled)

    # Evaluate model
    print("\n=== Model Evaluation ===")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
    print("✓ Saved confusion matrix: confusion_matrix.png")
    plt.show()

    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)

    plt.figure(figsize=(10, 8))
    sns.barplot(data=feature_importance.head(15), x='importance', y='feature')
    plt.title('Top 15 Feature Importances')
    plt.xlabel('Importance')
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
    print("✓ Saved feature importance: feature_importance.png")
    plt.show()

    return rf_model, scaler, feature_importance


def save_results(df, model, scaler, feature_importance):
    """Save analysis results."""
    print("\n=== Saving Results ===")

    # Save processed dataset
    df.to_csv('processed_dataset.csv', index=False)
    print("✓ Saved dataset: processed_dataset.csv")

    # Save feature importance
    feature_importance.to_csv('feature_importance.csv', index=False)
    print("✓ Saved feature importance: feature_importance.csv")

    # Create summary report
    report = {
        'dataset_shape': df.shape,
        'n_features': df.shape[1] - 1,
        'n_samples': df.shape[0],
        'target_classes': sorted(df['target'].unique()),
        'class_distribution': df['target'].value_counts().to_dict(),
        'top_5_features': feature_importance.head(5)['feature'].tolist()
    }

    # Save summary as JSON
    import json
    with open('analysis_summary.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    print("✓ Saved summary: analysis_summary.json")


def main():
    """Main analysis pipeline."""
    print("🤖 Machine Learning Analysis Pipeline")
    print("=" * 50)

    # Generate or load data
    df = generate_sample_data()

    # Explore data
    df = explore_data(df)

    # Create visualizations
    visualize_data(df)

    # Train model
    model, scaler, feature_importance = train_model(df)

    # Save results
    save_results(df, model, scaler, feature_importance)

    print("\n" + "=" * 50)
    print("✅ Analysis complete!")
    print("Files generated:")
    print("  - data_exploration.png")
    print("  - confusion_matrix.png")
    print("  - feature_importance.png")
    print("  - processed_dataset.csv")
    print("  - feature_importance.csv")
    print("  - analysis_summary.json")


if __name__ == "__main__":
    main()
