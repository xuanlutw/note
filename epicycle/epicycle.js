let r_ratio = 0.3;
let t_ratio = 2;
let orbit = [];
let l_orbit = [];
const radius = 120;
const l_radius = 245;
const c_x = 250;
const c_y = 250;

var sun = new Image();
var moon = new Image();
var looks = new Image();

function rad(degrees) {
    return (Math.PI/180) * degrees;
}

function now_coord(angle) {
    return [c_x + radius*Math.cos(angle) - r_ratio*radius*Math.sin((1+t_ratio)*angle), c_y + radius*Math.sin(angle) + r_ratio*radius*Math.cos((1+t_ratio)*angle)];
}

function normalize(old_coord) {
    old_coord[0] -= c_x;
    old_coord[1] -= c_y;
    old_r = Math.sqrt(old_coord[0] * old_coord[0] + old_coord[1] * old_coord[1]);
    norm_factor = l_radius / old_r;
    return [old_coord[0] * norm_factor + c_x, old_coord[1] * norm_factor + c_y];
}

function my_round(x) {
    return Math.round(x * 100)/100;
}

function update() {
    r_ratio = my_round(0.1 + 0.008 * document.getElementById("slider_r_ratio").value, 2);
    document.getElementById("r_ratio").innerHTML = (`Radius ratio: ${r_ratio}`);
    t_ratio = my_round(0.1 + 0.099 * document.getElementById("slider_t_ratio").value, 2);
    document.getElementById("t_ratio").innerHTML = (`Angulsr velocity ratio: ${t_ratio}`);
    orbit = [];
    l_orbit = [];
}

function init() {
    sun.src = 'dot.png';
    moon.src = 'dot.png';
    looks.src = 'dot.png';
    document.getElementById("slider_r_ratio").oninput = update();
    document.getElementById("slider_t_ratio").oninput = update();
    update();
    window.requestAnimationFrame(draw);
}

function draw() {
    ctx = document.getElementById('canvas').getContext('2d');
    ctx.globalCompositeOperation = 'destination-over';
    ctx.clearRect(0, 0, 2*c_x, 2*c_y); // clear canvas

    ctx.strokeStyle = 'rgba(0, 0, 0, 0.4)';
    
    // E
    ctx.save();
    ctx.translate(c_x, c_y);
    ctx.beginPath();
    ctx.arc(0, 0, radius, 0, Math.PI * 2, false);
    ctx.stroke();
    let time = new Date();
    angle = rad((time.getSeconds() + time.getMilliseconds()/1000) * 6);
    ctx.rotate(angle);
    ctx.translate(radius, 0);
    
    // M
    ctx.beginPath();
    ctx.arc(0, 0, r_ratio*radius, 0, Math.PI * 2, false);
    ctx.stroke();
    ctx.save();
    ctx.rotate(t_ratio * angle);
    ctx.translate(0, radius * r_ratio);
    ctx.drawImage(moon, -5, -5, 10, 10);
    ctx.restore();
    ctx.restore();

    orbit.push(now_coord(angle));
    if (orbit.length > 3000)
        orbit.shift();
    ctx.strokeStyle = 'rgba(255, 0, 0, 0.4)';
    ctx.beginPath();
    for (let i = 0;i < orbit.length;++i) {
        if (i)
            ctx.lineTo(orbit[i][0], orbit[i][1]);
        else
            ctx.moveTo(orbit[i][0], orbit[i][1]);
    }
    ctx.stroke();

    l_coord = normalize(now_coord(angle));
    ctx.drawImage(looks, l_coord[0]-5, l_coord[1]-5, 10, 10);
    l_orbit.push(l_coord);
    if (l_orbit.length > 3000)
        l_orbit.shift();
    ctx.strokeStyle = 'rgba(0, 255, 0, 0.4)';
    ctx.beginPath();
    for (let i = 0;i < l_orbit.length;++i) {
        if (i)
            ctx.lineTo(l_orbit[i][0], l_orbit[i][1]);
        else
            ctx.moveTo(l_orbit[i][0], l_orbit[i][1]);
    }
    ctx.stroke();

    ctx.drawImage(sun, c_x-5, c_y-5, 10, 10);

    window.requestAnimationFrame(draw);
}
