x1 = [0 0 20 60 10 40 65 43.5 85 85 85 85 0 32 64];
y1 = [0 30 0 0 79 79 79 46.5 69 57 45 33 84 84 84];
x2 = [0 0 20 60 10 40 65 43.5 85 85 85 85 0 32 64];
y2 = [30 45 12 24 84 84 84 49.5 80 68 56 44 94 94 94];
x3 = [20 18 30 96 25 55 80 51.5 93 93 93 93 32 64 96];
y3 = [30 45 12 24 84 84 84 49.5 80 68 56 44 94 94 94];
x4 = [20 18 30 96 25 55 80 51.5 93 93 93 93 32 64 96];
y4 = [0 30 0 0 79 79 79 46.5 69 57 45 33 84 84 84];

hold on
for (i = 1:length(x1))
    plot([x1(i) x2(i) x3(i) x4(i) x1(i)], [y1(i), y2(i), y3(i), y4(i) y1(i)], 'r-')
    hold on
end
axis square
axis([0, 96, 0, 96])