from src.data.load_letterboxd import load_letterboxd_data
from src.features.features import combine_letterboxd_data
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent
def main():
    watched_df, likes_df, profile_df = load_letterboxd_data()
    combined_df = combine_letterboxd_data(watched_df, likes_df, profile_df)

    print(combined_df.head())
    print(
        f"\nTotal watched: {len(combined_df)} | "
        f"Liked: {combined_df['Liked'].sum()} | "
        f"Favorites: {combined_df['Favorite'].sum()}"
    )

    # Save output into a dedicated processed folder
    combined_df.to_csv(PROJECT_ROOT / "my-data" / "processed" / "combined_letterboxd_data.csv", index=False)

if __name__ == "__main__":
    main()
