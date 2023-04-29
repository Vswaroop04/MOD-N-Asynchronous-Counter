from flask import Flask, request, render_template
import math
from tabulate import tabulate

app = Flask(__name__)


@app.route('/')
def result():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        a = int(request.form['a'])
        n = math.ceil(math.log(a, 2))
        b = a - 1

        # Convert decimal to binary
        number = int(b)
        decimal = int(number)
        binary = ''
        while decimal != 0:
            remainder = decimal % 2
            binary += str(remainder)
            decimal = int(decimal / 2)
        final_binary = binary[::-1]

        # Generate present state table
        def traverse_binary(n):
            binary_list = []
            for i in range(2**n):
                binary_num = bin(i)[2:].zfill(n)
                binary_list.append([int(bit) for bit in binary_num])
            return binary_list

        x = final_binary
        n = len(x)
        binary_arr = traverse_binary(n)

        # Generate next state table
        def add_one(binary_arr):
            next_arr = []
            for binary_num in binary_arr:
                new_num = []
                for bit in binary_num:
                    new_bit = (bit + 1) % 2
                    new_num.append(new_bit)
                next_arr.append(new_num)
            return next_arr

        next_arr = add_one(binary_arr)
        my_list = next_arr
        if len(my_list) > 1:
            for i in range(len(my_list) // 2):
                j = len(my_list) - i - 2
                my_list[i], my_list[j] = my_list[j], my_list[i]

        # Swap last element of next state table with binary equivalent of 'a'
        last_elem = my_list.pop()
        last_bin = [int(bit) for bit in bin(a-1)[2:].zfill(n)]
        my_list.append(last_bin)

        # Fill rows after 'b' element with 'x'
        b_index = b
        for i in range(b_index, len(my_list)):
            my_list[i] = ['0']*n
        for i in range(b_index+1, len(my_list)):
            my_list[i] = ['x']*n

        # Render the template with the results
       
        present_table = tabulate(binary_arr, headers=["q" + str(i) for i in range(n)], tablefmt="html")
        next_table = tabulate(my_list, headers=["Q" + str(i) for i in range(n)], tablefmt="html")
        
      
        return render_template('results.html', present_table=present_table, next_table=next_table)

    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)
