import matplotlib.pyplot as plt
import numpy as np
from japanmap import picture, get_data, pref_map

#都道府県をどの色で塗るのかを指定
pct: np.array = picture({
    "北海道": "yellow",
    "東京都": "yellow",
    "静岡県": "yellow"
})
plt.axis("off")
plt.imshow(pct)
plt.savefig("map.png")
plt.show()