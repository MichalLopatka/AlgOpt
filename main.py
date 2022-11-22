from loader import Loader


def main():
    loader = Loader(path="data/airland1.txt")
    print(loader.planes[2])
    print(loader.separation_matrix)


if __name__ == "__main__":
    main()
