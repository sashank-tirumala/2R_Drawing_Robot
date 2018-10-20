% DRAWSEG - Draws a series of line segments stored in an Nx4 array.
%
% Usage: drawseg(seglist, figNo, lw, col);
%                            
%         seglist - an Nx4 array storing line segments in the form
%                    [x1 y1 x2 y2
%                     x1 y1 x2 y2
%                         . .     ] etc 
%         figNo   - optional figure number
%         lw      - optional line width
%         col     - optional 3-vector specifying the colour
%
%
% See also:  EDGELINK, LINESEG, MAXLINEDEV, MERGESEG
%

% Peter Kovesi   
% School of Computer Science & Software Engineering
% The University of Western Australia
% pk @ csse uwa edu au
% http://www.csse.uwa.edu.au/~pk
%
% December 2000

function drawseg(seglist, figNo, lw, col);
    
    if nargin >= 2  && figNo ~= 0
	figure(figNo);
    end
    
    if nargin < 3
	lw = 1;
	col = [0 0 1];
    elseif nargin < 4
	col = [0 0 1];
    end
%    clf

    Nseg = size(seglist,1);

    hold on
    for s = 1:Nseg
	line([seglist(s,1) seglist(s,3)], [seglist(s,2) seglist(s,4)],...
	     'LineWidth',lw, 'Color',col);
	hold on
	plot([seglist(s,1) seglist(s,3)], [seglist(s,2) seglist(s,4)],'.'); 

    end

