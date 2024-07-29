from flask import Flask, render_template, request
import ast
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

r = 13
q = 31
l = 20
rvs = 16500
bin_list = [0,1,0,1,0,1,1,1,1,0,1,1,0,1,0,0,0,0,0,1,0,0,1,1,0,1,1,0,0,1,1]

@app.route('/run_function', methods=['POST'])
def run_function():
    if request.method == 'POST':
        r = int(request.form['r'])
        q = int(request.form['q'])
        l = int(request.form['l'])
        rvs = int(request.form['rvs'])
        bin_list = ast.literal_eval(request.form['bin_list'])
        ind = int(request.form['ind'])

        # call function with the input parameters
        uniforms = tausworthe(r, q, l, rvs, bin_list)
        val_at_ind = uniforms[ind]
        count_unif = len(uniforms)

        return render_template('results.html', count = count_unif, val_at_index = val_at_ind, results=uniforms)

# create tausworthe generator with default bin_list above. if bin_list is specified, use that bin_list
def tausworthe(r, q, l, rvs, bin_list=bin_list):
    length = (rvs * l) - q
    for i in range(length):
        len_bin = len(bin_list)
        if bin_list[len_bin - q] == bin_list[len_bin - r]:
            bin_list.append(0)
        else:
            bin_list.append(1)

    counter = l
    add_bits = []
    unif_list = []
    
    for i in bin_list:
        counter -= 1
        value = (2 ** counter) * i
        add_bits.append(value)
        if counter == 0:
            counter = l

    counter = l
    for i, elem in enumerate(add_bits):
        counter -= 1
        if counter == 0:
            slice_index = i + 1 - l
            value = np.floor(sum(add_bits[slice_index:i+1]) / (2 ** l) * 70)
            unif_list.append(value)
            counter = l

    return unif_list

if __name__ == '__main__':
    app.run(debug=True)