from flask import Flask, request
import csv
import os
import time

app = Flask(__name__)

save_path = "/Users/xicheng/Desktop/data"
csv_filename = None

@app.route('/sensor/RES', methods=['POST'])
def receive_csv_data():
    try:
        csv_data = request.form.get('csv_data')

        if csv_data:
            global csv_filename
            if csv_filename is None:
                current_time = int(time.time())
                csv_filename = f"res_{current_time}.csv"

                os.makedirs(save_path, exist_ok=True)

            file_path = os.path.join(save_path, csv_filename)

            # Write CSV data into the file
            with open(file_path, "a", newline="", encoding="utf-8") as csv_file:
                csv_file.write(csv_data + "\n")

            return "Data received and saved successfully.", 200
        else:
            return "No CSV data received.", 400

    except Exception as e:
        return f"Error processing data: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
