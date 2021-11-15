from app import app

def main() -> int:
    app.run(debug=True)

if __name__ == '__main__':
    sys.exit(main())
