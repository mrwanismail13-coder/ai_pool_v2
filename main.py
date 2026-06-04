from run_overlay import run

if __name__ == "__main__":
    try:
        run()

    except Exception as e:
        print("ERROR:", e)
        input("Press Enter to exit...")
