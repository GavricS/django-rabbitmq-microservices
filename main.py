import time

def main():
    i = 1
    while True:
        print(f"Hello, world #{i}")
        i += 1
        time.sleep(1)

if __name__ == "__main__":
    main()