import numpy as np
import matplotlib.pyplot as plt
import random as acak
import math
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

# inisialisasi awal
window = None
random = 0
input_entries = []
temp_entries = []
input_delete = []
temp_delete = []
input_random = []
gantiMode = 0
city_label = []
delete_label = []
posisiKota = [[-24, 11], [-24, 6], [-24, 0], [-21, -6], [-19, 1],
              [-18, 10], [-18, -3], [-14, 0], [-14, -5], [-13, 10],
              [-11, 5], [-9, 0], [-9, -6], [-4, 11], [-4, 7],
              [-3, 3], [-3, -8], [-2, -1], [-1, -4], [1, 9],
              [1, -10], [3, 4], [3, -1], [4, -5], [4, -10],
              [6, 7], [6, -7], [7, 2], [9, 1], [9, -4],
              [9, -7], [10, -2], [11, 6], [12, -7], [14, 0],
              [14, -6], [14, -13], [16, -2], [16, -4], [17, 2],
              [19, 5], [19, 0], [21, 2], [22, 7], [22, 4],
              [22, 3], [25, 8]]
figG = None
axG = None
lineG = None
canvasG = None

def ant_colony(jumlahIterasi, jumlahSemut, alpha, beta, evaporationRate, posisiKota, tambahKota, hapusKota):
    # disorting descending untuk delete citynya
    tempKota = []
    if (hapusKota != None):
        for i in range(len(hapusKota)):
            tempKota.append(eval(hapusKota[i].get()))

    tempKota.sort(reverse=True)

    # untuk tambah kotanya
    if (tambahKota != None):
        for i in range(len(tambahKota)):
            posisiKota.append(tambahKota[i])

    # untuk delete citynya
    if (tempKota != None):
        for i in range(len(tempKota)):
            del posisiKota[abs(tempKota[i] - 1)]

    posisiKota = np.array(posisiKota)
    print(posisiKota)

    jumlahKota = len(posisiKota)

    # buat matriks seukuran jumlahKota x jumlahKota yang isi awalnya semua 0
    matrix = np.zeros((jumlahKota, jumlahKota))
    # print(matrix)

    # loop untuk hitung jarak tiap kota dari koordinat random hasil posisiKota akar (x2-x1)^2 + (y2-y1)^2
    for i in range(jumlahKota):
        for j in range(jumlahKota):
            matrix[i][j] = math.sqrt(
                math.pow(posisiKota[j][0] - posisiKota[i][0], 2) + math.pow(posisiKota[j][1] - posisiKota[i][1], 2))
    # print(matrix)

    # inisialisai matriks pheromonenya
    pheromoneMatrix = np.ones((len(matrix), len(matrix)))
    best_path = None
    best_path_length = np.inf

    for iterasi in range(jumlahIterasi):
        paths = []
        path_lengths = []
        for semut in range(jumlahSemut):
            # list visited untuk pengecekan kota mana aja yang udah dikunjungi sama semut
            # path nya nanti untuk nyimpen rutenya si semut
            path = []
            visited = [False] * len(matrix)
            current = np.random.randint(len(matrix))
            visited[current] = True
            path.append(current)
            length = 0
            while (check_any_unvisited(visited)):
                next_kota = pilih_next_kota(current, visited, alpha, beta, pheromoneMatrix, matrix)
                path.append(next_kota)
                length += matrix[current][next_kota]
                visited[next_kota] = True
                current = next_kota
            # ini paths ujung2nya nyimpen rute yg dilewati tiap semut per iterasi, klo path_lengths dia nyimpen length diap path semut per iterasi
            # balek ke titik awal
            path.append(path[0])
            length += matrix[current][path[0]]

            paths.append(path)
            path_lengths.append(length)

            # pengecekan mana path sama length terpendek
            if length < best_path_length:
                best_path = path
                best_path_length = length

        # ini kalo di rumusnya itu baru kali evaporationnya doang
        pheromoneMatrix *= evaporationRate

        # ini untuk delta pheromonenya berdasarkan rute yang dilewati semut k
        for i in range(jumlahSemut):
            for j in range(jumlahKota):
                pheromoneMatrix[paths[i][j]][paths[i][j + 1]] += 1 / path_lengths[i]

        # visualisasinya
        if (iterasi % 10 == 0):
            figG = plt.Figure(figsize=(6, 4), dpi=100)
            axG = figG.add_subplot(111)

            print(best_path)
            print(best_path_length)
            color_map = plt.cm.get_cmap('tab20')

            plt.ion()

            axG.set_xlabel('X -- Best path length: {}'.format(best_path_length))
            axG.set_ylabel('Y')

            axG.set_title('Ant Colony Optimization - Traveling Salesman Problem (iterasi ke {})'.format(iterasi))
            axG.scatter(posisiKota[:, 0], posisiKota[:, 1], color='blue', label='posisiKota')
            axG.plot(posisiKota[best_path, 0], posisiKota[best_path, 1], color='red', linestyle='-', linewidth=1.5,
                     label='Best Tour')
            for i in range(len(paths)):
                color = color_map(i)
                axG.plot(posisiKota[paths[i], 0], posisiKota[paths[i], 1], color=color, linestyle='--', linewidth=1,
                         alpha=0.3, label='semut {}'.format(i + 1))
            axG.legend()
            plt.close(figG)

            canvasG = FigureCanvasTkAgg(figG, master=window)
            canvasG.draw()
            canvasG.get_tk_widget().grid(row=0, column=0, columnspan=2)

            window.update()

            time.sleep(3)

        if (iterasi + 1 == jumlahIterasi):
            figG = plt.Figure(figsize=(6, 4), dpi=100)
            axG = figG.add_subplot(111)

            print(best_path_length)
            color_map = plt.cm.get_cmap('tab20')

            plt.ion()

            axG.set_xlabel('X -- Best path length: {}'.format(best_path_length))
            axG.set_ylabel('Y')

            axG.set_title('Ant Colony Optimization - Traveling Salesman Problem (iterasi ke {})'.format(iterasi + 1))
            axG.scatter(posisiKota[:, 0], posisiKota[:, 1], color='blue', label='posisiKota')
            axG.plot(posisiKota[best_path, 0], posisiKota[best_path, 1], color='red', linestyle='-', linewidth=1.5,
                     label='Best Tour')
            for i in range(len(paths)):
                color = color_map(i)
                axG.plot(posisiKota[paths[i], 0], posisiKota[paths[i], 1], color=color, linestyle='--', linewidth=1,
                         alpha=0.3, label='semut {}'.format(i + 1))
            axG.legend()

            canvasG = FigureCanvasTkAgg(figG, master=window)
            canvasG.draw()
            canvasG.get_tk_widget().grid(row=0, column=0, columnspan=2)

            window.update()


def check_any_unvisited(arr):
    if False in arr:
        return True
    else:
        return False

# fungsi untuk pemilihan next kotanya
def pilih_next_kota(current, visited, alpha, beta, pheromone, matrix):
    length = len(visited)
    yang_belum_divisit = []
    # Cek sudah visited / belum, kalo blom masukin ke array
    for i in range(length):
        if visited[i] == False:
            yang_belum_divisit.append(i)
    arr_probabilitas = []
    total = 0

    for kota in yang_belum_divisit:
        pheromone_level = pheromone[current][kota]
        attraction = 1.0 / matrix[current][kota]
        probabilitas = pheromone_level ** alpha * attraction ** beta
        arr_probabilitas.append(probabilitas)
        total += probabilitas

    arr_probabilitas = [probabilitas / total for probabilitas in arr_probabilitas]
    next_kota = np.random.choice(yang_belum_divisit, p=arr_probabilitas)
    return next_kota

# function add city yang connect ke UI
def add_city():
    global window, input_entries, temp_entries, city_label
    label = tk.Label(window, text="City:")
    label.grid(row=len(temp_entries) + 1 + 10, column=0)
    city_entry = tk.Entry(window)
    city_entry.grid(row=len(temp_entries) + 1 + 10, column=1)
    input_entries.append(city_entry)
    temp_entries.append(city_entry)
    city_label.append(label)

# function delete city yang connect ke UI
def delete_city():
    global window, input_entries, temp_entries, city_label, temp_delete, delete_label
    labelDelete = tk.Label(window, text="Delete City ke:")
    labelDelete.grid(row=len(temp_delete) + 1 + 10, column=2)
    city_delete = tk.Entry(window)
    city_delete.grid(row=len(temp_delete) + 1 + 10, column=3)
    input_delete.append(city_delete)
    temp_delete.append(city_delete)
    delete_label.append(labelDelete)

def finish():
    global window, input_entries, posisiKota
    generate_button.configure(state='normal')
    for entry in input_entries:
        entry.configure(state='disabled')
    for delete in input_delete:
        delete.configure(state='disabled')
    if (random == 1):
        input_random.append(randomgen_labels)
        for entry in input_random:
            temp = eval(entry.get())
        print(temp)
        posisiKota = np.random.rand(acak.randint(temp[0], temp[1]), 2)
        posisiKota = posisiKota.tolist()
        update_label()


def generate_graph():
    # Get user input
    global input_entries, posisiKota, city_label, input_delete, canvasG
    if (selected_option.get() == "1. Hardcode"):
        random = 0
    elif (selected_option.get() == "2. Random"):
        random = 1
    jumlahIterasi = int(iterasi_label.get())
    jumlahSemut = int(semut_label.get())
    alpha = float(alpha_label.get())
    beta = float(beta_label.get())
    evaporationRate = float(evaporation_label.get())

    # memasukkan data kota yang di add oleh user
    for entry in input_entries:
        posisiKota.append(eval(entry.get()))

    # pemanggilan functionnya
    if (len(input_delete) != 0):
        ant_colony(jumlahIterasi, jumlahSemut, alpha, beta, evaporationRate, posisiKota, None, input_delete)
    else:
        ant_colony(jumlahIterasi, jumlahSemut, alpha, beta, evaporationRate, posisiKota, None, None)

    update_label()

    input_entries = []
    input_delete = []

def update_label():
    value = len(posisiKota)
    # Update the label text
    labelJumlahKota.config(text="Jumlah Kota: " + str(value))

def clear_label():
    # Update the label text
    labelJumlahKota.config(text="Jumlah Kota: ")


# buat tkinter window
window = tk.Tk()
window.title("Ant Colony Optimization")


def select_option(option):
    global posisiKota, random
    print("Selected option:", option)
    for label in city_label:
        label.grid_forget()
    for entry in temp_entries:
        entry.grid_forget()
    for labeld in delete_label:
        labeld.grid_forget()
    for delete in temp_delete:
        delete.grid_forget()
    if (option == "1. Hardcode"):
        random = 0
        randomgen_labels.delete(0, tk.END)
        randomgen_labels.configure(state='disable')
        posisiKota = [[-24, 11], [-24, 6], [-24, 0], [-21, -6], [-19, 1],
                      [-18, 10], [-18, -3], [-14, 0], [-14, -5], [-13, 10],
                      [-11, 5], [-9, 0], [-9, -6], [-4, 11], [-4, 7],
                      [-3, 3], [-3, -8], [-2, -1], [-1, -4], [1, 9],
                      [1, -10], [3, 4], [3, -1], [4, -5], [4, -10],
                      [6, 7], [6, -7], [7, 2], [9, 1], [9, -4],
                      [9, -7], [10, -2], [11, 6], [12, -7], [14, 0],
                      [14, -6], [14, -13], [16, -2], [16, -4], [17, 2],
                      [19, 5], [19, 0], [21, 2], [22, 7], [22, 4],
                      [22, 3], [25, 8]]
        update_label()
    if (option == "2. Random"):
        randomgen_labels.configure(state='normal', background="light cyan")
        generate_button.configure(state='disable')
        random = 1
        clear_label()

# untuk dropdown random atau hardcode
def on_option_changed(*args):
    selectedd_option = selected_option.get()
    select_option(selectedd_option)

options = ["1. Hardcode", "2. Random"]
selected_option = tk.StringVar(window)
selected_option.set(options[0])

dropdown = tk.OptionMenu(window, selected_option, *options, command=on_option_changed)
dropdown.grid(row=1, column=0)

# Iterasi input
iterasi_label = tk.Label(window, text="Jumlah Iterasi:", background="cyan4").grid(row=2, column=0, sticky="w")
iterasi_label = tk.Entry(window, background="cyan4")
iterasi_label.grid(row=2, column=1)

# Jumlah Semut input
semut_label = tk.Label(window, text="Jumlah Semut:", background="cyan3").grid(row=3, column=0, sticky="w")
semut_label = tk.Entry(window, background="cyan3")
semut_label.grid(row=3, column=1)

# Alpha input
alpha_label = tk.Label(window, text="Alpha:", background="cyan2").grid(row=4, column=0, sticky="w")
alpha_label = tk.Entry(window, background="cyan2")
alpha_label.grid(row=4, column=1)

# Beta input
beta_label = tk.Label(window, text="Beta:", background="cyan").grid(row=5, column=0, sticky="w")
beta_label = tk.Entry(window, background="cyan")
beta_label.grid(row=5, column=1)

# Evaporation Rate input
evaporation_label = tk.Label(window, text="Evaporation Rate:", background="violetred2").grid(row=6, column=0, sticky="w")
evaporation_label = tk.Entry(window, background="violetred2")
evaporation_label.grid(row=6, column=1)

# Radnom city generate input
randomgen_label = tk.Label(window, text="Random jumlah city:", background="darkviolet").grid(row=7, column=0, sticky="w")
randomgen_labels= tk.Entry(window, background="darkviolet")
randomgen_labels.grid(row=7, column=1)
randomgen_labels.configure(state='disable')

# Add city button
add_city_button = tk.Button(window, text="Add City", command=add_city, background="green")
add_city_button.grid(row=10, column=1)

# delete city button
delete_city_button = tk.Button(window, text="Delete City", command=delete_city, background="red")
delete_city_button.grid(row=10, column=3)

# label yang menunjukkan jumlah kota
labelJumlahKota = tk.Label(window, text="Jumlah Kota: ", foreground="white", background="blue")
labelJumlahKota.grid(row=10, column=4, sticky="w")

update_label()

# Finish button
finish_button = tk.Button(window, text="Set the parameters (Click every changes you made)", command=finish)
finish_button.grid(row=8, column=1)

# Generate graph button
generate_button = tk.Button(window, text="Generate Graph", command=generate_graph, state='disabled')
generate_button.grid(row=9, column=1)

# Run the tkinter event loop
window.mainloop()