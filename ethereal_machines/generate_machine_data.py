import random
import time
from datetime import datetime
import mysql.connector 

# Database connection details
db_config = {
    'host': '127.0.0.1',  # Replace with your host
    'user': 'root',       # Replace with your user
    'password': 'Root@123',  # Replace with your password
    'database': 'machines'  # Replace with your DB name
}

# Function to generate field values based on given range
def generate_value(range_str):
    if range_str == 'CONSTANT':
        return None  # No change for constant values
    elif 'to' in range_str:
        low, high = map(float, range_str.split(' to '))
        return random.uniform(low, high)
    else:
        return float(range_str)

# Function to push data to MySQL database
def push_to_db(query, data):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(query, data)
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Simulate updates based on the "UPDATE INTERVAL"
def simulate_updates(machines_data, axes_data, iterations=10):
    for i in range(iterations):
        # Machine field updates
        for machine in machines_data:
            for field in machine['fields']:
                new_value = generate_value(field['range'])
                if new_value is not None:
                    field['value'] = new_value
                    # Insert into Field_Updates table
                    query = """
                        INSERT INTO Field_Updates (entity_type, entity_id, field_name, field_value, update_time)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    data = ('machine', machine['machine_id'], field['name'], new_value, datetime.now())
                    push_to_db(query, data)
        
        # Axis field updates
        for axis in axes_data:
            for field in axis['fields']:
                new_value = generate_value(field['range'])
                if new_value is not None:
                    field['value'] = new_value
                    # Insert into Field_Updates table
                    query = """
                        INSERT INTO Field_Updates (entity_type, entity_id, field_name, field_value, update_time)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    data = ('axis', axis['axis_id'], field['name'], new_value, datetime.now())
                    push_to_db(query, data)

        # Simulate real-time updates by adding a delay
        time.sleep(5)  # Adjust based on needs

# Example machine and axis data generation for 20 machines and 5 axes each
def generate_machines_and_axes():
    machines_data = []
    axes_data = []
    axis_names = ['X', 'Y', 'Z', 'A', 'C']

    # Generate 20 machines
    for machine_id in range(1, 21):
        machine = {
            'machine_id': machine_id,
            'machine_name': f'Machine_{machine_id}',
            'fields': [
                {'name': 'tool_offset', 'range': '5 to 40', 'value': 14.5},
                {'name': 'feedrate', 'range': '0 to 20000', 'value': 10000},
                {'name': 'tool_in_use', 'range': '1 to 24', 'value': 4}
            ]
        }
        machines_data.append(machine)

        # Generate 5 axes for each machine
        for axis_name in axis_names:
            axis = {
                'axis_id': len(axes_data) + 1,
                'machine_id': machine_id,
                'axis_name': axis_name,
                'fields': [
                    {'name': 'actual_position', 'range': '-190 to +190', 'value': random.uniform(-190, 190)},
                    {'name': 'max_acceleration', 'range': '0 to 200', 'value': random.uniform(0, 200)},
                    {'name': 'max_velocity', 'range': '0 to 100', 'value': random.uniform(0, 100)}
                ]
            }
            axes_data.append(axis)
    
    return machines_data, axes_data

# Generate machines and axes
machines_data, axes_data = generate_machines_and_axes()

# Simulate updates for machines and axes
simulate_updates(machines_data, axes_data, iterations=5)
