function [seglist] = final_result(image1,thresh,smooth)
%Should result in line segments that link the image
%   Uses code from petr ziowski website
im = imread(image1);
% im = rgb2gray(im);
edgeim = edge(im,'canny',thresh,smooth);

[edgelist, labelededgeim] = edgelink(edgeim, 1);
% Fit line segments to the edgelists
tol = 5;         % Line segments are fitted with maximum deviation from
         % original edge of 2 pixels.
seglist = lineseg(edgelist, tol);

% Draw the fitted line segments stored in seglist in figure window 3 with
% a linewidth of 2 and random colours
%drawedgelist(seglist, size(im), 2); axis off;
drawseg(seglist);
end

