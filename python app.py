from flask import Flask, request, jsonify
from flask_cors import CORS
import math
import sympy as sp
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route('/api/arithmetic/add', methods=['POST'])
def add_numbers():
    data = request.json
    numbers = data.get('numbers', [])
    result = sum(numbers)
    return jsonify({'result': result})

@app.route('/api/arithmetic/subtract', methods=['POST'])
def subtract_numbers():
    data = request.json
    numbers = data.get('numbers', [])
    result = numbers[0] - sum(numbers[1:])
    return jsonify({'result': result})

@app.route('/api/arithmetic/multiply', methods=['POST'])
def multiply_numbers():
    data = request.json
    numbers = data.get('numbers', [])
    result = 1
    for num in numbers:
        result *= num
    return jsonify({'result': result})

@app.route('/api/arithmetic/divide', methods=['POST'])
def divide_numbers():
    data = request.json
    numbers = data.get('numbers', [])
    if 0 in numbers[1:]:
        return jsonify({'error': 'Division by zero'}), 400
    result = numbers[0]
    for num in numbers[1:]:
        result /= num
    return jsonify({'result': result})

@app.route('/api/algebra/solve-linear', methods=['POST'])
def solve_linear():
    data = request.json
    equation = data.get('equation', '')
    try:
        x = sp.Symbol('x')
        eq = sp.sympify(equation.replace('=', '-(') + ')')
        solution = sp.solve(eq, x)
        return jsonify({'solutions': [float(sol) for sol in solution]})
    except:
        return jsonify({'error': 'Invalid equation'}), 400

@app.route('/api/algebra/solve-quadratic', methods=['POST'])
def solve_quadratic():
    data = request.json
    a, b, c = data.get('a'), data.get('b'), data.get('c')
    discriminant = b**2 - 4*a*c
    if discriminant > 0:
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)
        return jsonify({'solutions': [x1, x2], 'type': 'real'})
    elif discriminant == 0:
        x = -b / (2*a)
        return jsonify({'solutions': [x], 'type': 'real'})
    else:
        real = -b / (2*a)
        imag = math.sqrt(-discriminant) / (2*a)
        return jsonify({
            'solutions': [{'real': real, 'imag': imag}, {'real': real, 'imag': -imag}],
            'type': 'complex'
        })

@app.route('/api/matrix/operations', methods=['POST'])
def matrix_operations():
    data = request.json
    operation = data.get('operation')
    matrix_a = np.array(data.get('matrixA'))
    matrix_b = np.array(data.get('matrixB')) if data.get('matrixB') else None
    
    try:
        if operation == 'add':
            result = matrix_a + matrix_b
        elif operation == 'subtract':
            result = matrix_a - matrix_b
        elif operation == 'multiply':
            result = np.dot(matrix_a, matrix_b)
        elif operation == 'determinant':
            result = np.linalg.det(matrix_a)
        elif operation == 'inverse':
            result = np.linalg.inv(matrix_a)
        else:
            return jsonify({'error': 'Invalid operation'}), 400
        
        return jsonify({'result': result.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
