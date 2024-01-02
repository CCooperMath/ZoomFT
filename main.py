#! /usr/bin/env python
from website import initialize

app = initialize()

if __name__ == '__main__':
    app.run(debug=True)
