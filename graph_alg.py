import numpy as np
import matplotlib.pyplot as plt

x = ['AES', 'DES', '3DES', 'Blowfish', 'Twofish']
y_ = [0.06, 0.6, 11.74, 0.47, 19.76]

fig, ax = plt.subplots()
colors = ['red', 'purple', 'yellow', 'blue', 'silver']
ax.bar(x, y_, color=colors)
#plt.title('Время шифрования, сек.')

ax.set_xlabel('Алгоритмы шифрования', fontsize=12)
ax.set_ylabel('Время шифрования, сек.', fontsize=12)
k = 0
for rect in ax.patches:
    # Find where everything is located
    height = rect.get_height()
    width = rect.get_width()
    x = rect.get_x()
    y = rect.get_y()

    # The width of the bar is the count value and can used as the label
    label_text = y_[k]
    k += 1

    label_x = x + width / 3
    label_y = height + 0.6

    # don't include label if it's equivalently 0
    if width > 0.001:
        ax.annotate(label_text, xy=(label_x, label_y), va='center', xytext=(2, -1), textcoords='offset points')

#ax.set_facecolor('seashell')
#fig.set_facecolor('floralwhite')
fig.set_figwidth(10)    #  ширина Figure
fig.set_figheight(6)    #  высота Figure

plt.show()