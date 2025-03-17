import os

def main():
    for i in range(5):
        os.system("python generate.py")
        os.system("python simulate.py")

if __name__ == "__main__":
    main()