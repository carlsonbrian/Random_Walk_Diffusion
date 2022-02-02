% Setting fixed parameter values
X_Locs = 2 * 350;                               % Even number of prtcl lctns
Max_Points = 1000;                              % Init num of prtcls @ left lctns
Min_Points = 0;                                 % Init num of prtcls @ right lctns
N_Frames = 10000;                               % Num of times to recalculate dist

% Creating the initial distribution of particles from which
%  we start the diffusion simulation
X = linspace(1,X_Locs,X_Locs);                      % Int array of x locations
YA = Max_Points * ones(1,X_Locs/2);                 % Prtcls on left half
YB = Min_Points * ones(1,X_Locs/2);                 % Prtcls on right half
Y = [YA,YB];                                        % Prtcls for all x lctns
Y0= Y;                                              % Save init distribution
Spread = zeros(1,N_Frames);                         % To track profile spread

% Setting rng seed, printing out initial number of particles and
%  setting how often to print out simulation progress
seed = 1;                                           % Seed num to start rng
rng(seed);                                          % Intitializing rng
disp(['Total number of particles at start is ' ...
    num2str(sum(Y))]);
NN = 4;                                             % Num times to print prog
tic                                                 % Mark time at start of sim

% Calculate the particle profiles at each time point
for i = 1:N_Frames
    Z = zeros(1,X_Locs);                            % Allocate next prtcl prfl
    % Print out progress at the desgnated intervals
    if(i ~= 0 && mod(i,N_Frames/NN) == 0)
        disp([num2str(i) ' out of ' num2str(N_Frames) ...
            ' frames; elapsed minutes = ' num2str(toc) ...
            ' seconds'])
    end
    % Here we run through each x location and move particles by random walk
    for j = 1:X_Locs
        % In the first x position we either stay or move to the right
        if (j == 1)
            for k = 1:Y(1)
                if (rand(1) < 0.5) 
                    Z(1) = Z(1) + 1;                % Stays at first location
                else
                    Z(2) = Z(2) + 1;                % Moves right
                end
            end
        % At the last x position we either stay or move to the left
        elseif (j == X_Locs)
            for k = 1:Y(X_Locs)
                if (rand(1) < 0.5)
                    Z(X_Locs) = Z(X_Locs) + 1;      % Stays at last location
                else
                    Z(X_Locs-1) = Z(X_Locs-1) + 1;  % Moves left
                end
            end
        % In the middle locations either move left or right        
        else
            for k = 1:Y(j)
                if rand(1) < 0.5
                    Z(j-1) = Z(j-1) + 1;            % Moves left
                else
                    Z(j+1) = Z(j+1) + 1;            % Moves right
                end
                
            end
        end
    end
    Y = Z;                                          % Now save Z as new Y 
    
    % Now calculate the spread for the recently calculated profile
    index_1 = 0;
    index_2 = 0;
    for j = 1:X_Locs
        if (index_1 == 0 && Z(j) <= (0.75*Max_Points))
            index_1 = j;
        end
        if (index_2 == 0 && Z(j) < (0.25*Max_Points))
            index_2 = j;
        end
        
    end
    
    Spread(i) = index_2 - index_1;
    
end

% The simulation of the evolution of the diffusion is complete
%  so now we echo the final simulation time, statistics and make plots

% Final simulation time
disp([num2str(i) ' out of ' num2str(N_Frames) ...
    ' frames; elapsed minutes = ' num2str(toc) ...
    ' seconds'])

% Statistics
disp(['Total number of particles at end = ' num2str(sum(Y))])
disp(['Number of particles in first half = ' num2str(sum(Y(1:X_Locs/2)))])
disp(['Number of particles in second half = ' num2str(sum(Y(X_Locs/2:X_Locs)))])
disp(['Spread in final profile (3/4 to 1/4) = ' num2str(index_2 - index_1)])

% Plots - Initial and final profile then Spread as a function of frame number
figure(1)
plot(X,Y0,'-g')                                         % Intital profile
hold on
plot(X,Y,'.k','MarkerSize',6)                           % Final profile
xlim([1 X_Locs])
ylim([0 1.2*Max_Points])
xlabel('X Location')
ylabel('Number of Particles')
title('Simulation of 1-D Particle Diffusion Starting from a Step Distribution')
% savefig("Example4_1a.png,dpi=200)
%%
figure(2)
N_FramesVect = 1:1:N_Frames;
plot(N_FramesVect,Spread,'.k','MarkerSize',1)
xlim([1 N_Frames])
ylim([0 1.6*sqrt(N_Frames)])
xlabel('Frame Number (Time)')
ylabel('Spread of Profile (3/4 to 1/4)')
title('Simulation of 1-D Particle Diffusion Starting from a Step Distribution')
% savefig("Example4_1b.png,dpi=200)