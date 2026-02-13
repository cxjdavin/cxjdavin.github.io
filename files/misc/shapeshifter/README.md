# Setup

1. Install Google's [ortools](https://developers.google.com/optimization/) (for constraint optimisation) and jsonpickle (for saving state)

  `pip3 install ortools jsonpickle`

2. Open [Shapeshifter game](http://www.neopets.com/medieval/shapeshifter_instruct.phtml) in Chrome. Login if required.

3. Open Developer tools

# Instructions (for each game level)

1. Copy paste `shapeshifter.js` into console

2. Copy output into `main` of `shapeshifter.py`

3. Run `python3 shapeshifter.py`

4. Manually click the grids according to the output. Coordinates given refer to *top left* of the bounding box of each pattern

# Known issues

- May need to change `seq_idx`, `boardElem_idx`, `activeShape_idx`, `nextShapes_idx` based on state of Neopets account. Depending on what other boxes does your account screen have, look at `tbodys`. Run the following:
```
const content = document.getElementById('content');
const tbodys = content.firstElementChild.firstElementChild.getElementsByTagName('tbody');
tbodys;
```
Then, mouseover to figure out and replace the idx appropriately

- If "Hint" box pops up, need to refresh page before `shapeshifter.js` script can work, because it messes up the indexing
