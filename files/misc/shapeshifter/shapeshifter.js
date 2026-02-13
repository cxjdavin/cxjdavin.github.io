const content = document.getElementById('content');
const tbodys = content.firstElementChild.firstElementChild.getElementsByTagName('tbody');

var seq_idx = 8;
var boardElem_idx = 6;
var activeShape_idx = 10;
var nextShapes_idx = 11;

const level = document.getElementsByTagName('big')[0].innerText.split(" ")[1];
const sequence = tbodys[seq_idx].getElementsByTagName('td');
const map = new Map();
map.set(sequence[sequence.length-3].firstElementChild.src, map.size);
for (let i = 0; i < sequence.length - 3; i += 2) {
    map.set(sequence[i].firstElementChild.src, map.size);
}

const states = Array.from(Array(map.size).keys());

const boardElem = tbodys[boardElem_idx].children;
const board = [];
for (let i = 0; i < boardElem.length; i++) {
    const row = boardElem[i].children;
    board[i] = [];
    for (let j = 0; j < row.length; j++) {
        const cell = row[j];
        // to highlight a cell's border
        // cell.setAttribute("style", "border: 1px solid blue;");
        board[i][j] = map.get(cell.firstElementChild.firstElementChild.src);
    }
}

const activeShape = tbodys[activeShape_idx].children;
const shapes = [];
shapes[0] = [];
for (let i = 0; i < activeShape.length; i++) {
    const row = activeShape[i].children;
    shapes[0][i] = [];
    for (let j = 0; j < row.length; j++) {
        const cell = row[j];
        const img = cell.firstChild;
        shapes[0][i][j] = img ? 1 : 0;
    }
}

const nextShapes = tbodys[nextShapes_idx] ? tbodys[nextShapes_idx].getElementsByTagName('tbody') : [];
for (let k = 0; k < nextShapes.length; k++) {
    const shape = nextShapes[k].children;
    shapes[1 + k] = [];
    for (let i = 0; i < shape.length; i++) {
        let row = shape[i].children;
        shapes[1 + k][i] = [];
        for (let j = 0; j < row.length; j++) {
            const cell = row[j];
            const img = cell.firstChild;
            shapes[1 + k][i][j] = img ? 1 : 0;
        }
    }
}

let s = "level = " + level + ";\n";
s += "states = [" + states + "];\n"
s += "grid = [[";
s += board.map((row) => (row.join(', '))).join('],[');
s += ']]\n';
s += '\n';
s += 'patterns = []\n';
shapes.forEach((shape) => {
    s += 'patterns.append(Pattern((' + shape.length + ', ' + shape[0].length + '), [[';
    s += shape.map((row) => (row.join(', '))).join('],[');
    s += ']]))\n'
});

console.log(s);
