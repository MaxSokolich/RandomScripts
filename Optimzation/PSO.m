clc;
clear;
close all;

%% Problem Definition

CostFunc = @(x) CostFunction(x);                                           % We can change Cost function at any time in the future
                                                                           % All 5 of our deicsion variables are real numbers ranging from -10 to 10                                                                      % so our search space is the 5x5 cartesiion product of this range to itself
nVar = 2;                                                                  % Number of Unknown (Decision) Variables

VarSize = [1 nVar];                                                        % Matrix Size of Decision Variables 

VarMin = -10;                                                                % Lower Bound of Decision Variables 

VarMax = 10;                                                                % Upper Bound of Decision Variables


%% Parameter of PSO
MaxIt = 50;                                                                 % Maximum Number of Generations (Iterations)

nPop = 30;                                                                  % Population Size (Swarm Size) (# of Particles)

c1 = .2;
c2 = .2;
w = .8;                                                                   % Social or Global Coefficient


%% Initialization

% Each particle will have position, velocity, personal best position, and personal best cost
Empty_Particle.Position = [];
Empty_Particle.Velocity = [];
Empty_Particle.Cost = [];
Empty_Particle.Best.Position = [];
Empty_Particle.Best.Cost = [];

% Repeat Template to create array of empty particles
Particle = repmat(Empty_Particle, nPop, 1);                                % Array of Empty Particles (repmat(matrix, #rows, #columns)

GlobalBest.Cost = Inf;



clr = ['r','g','b','c','m','y','k'];
[X,Y] = meshgrid(linspace(VarMin,VarMax),linspace(VarMin,VarMax));
Z = CostFunction(X,Y);

for i = 1:nPop
    
    % Generate Random Solution
    Particle(i).Position = (VarMax * rand(VarSize) + VarMin * rand(VarSize));
    disp(Particle(i).Position);
    % Evalaute Each Particle
    Particle(i).Cost = CostFunction(Particle(i).Position(1), Particle(i).Position(2));
    
    % Initilize Velocity
    Particle(i).Velocity = zeros(VarSize); 
    
    % The personal best position and cost are the same as the current pos and cost
    Particle(i).Best.Position = Particle(i).Position;
    Particle(i).Best.Cost = Particle(i).Cost;
    
  
 
    % Update Global Best
    if Particle(i).Best.Cost < GlobalBest.Cost
       GlobalBest = Particle(i).Best;  
  
    end
    
    
end

% Array to Hold Best Cost Values at Each Iteration
BestCosts = zeros(MaxIt, 1);

InitialParticles = repmat(Particle,1);




%% Main Loop of PSO
figure; 
x0=0;
y0=0;
width=1080;
height=1440;
set(gcf,'position',[x0,y0,width,height])
contourf(X,Y,Z,10);
InterestParticle = 1;  % Single out a particle to track
hold on
xlim([VarMin,VarMax])
ylim([VarMin,VarMax])
for gen = 1:MaxIt
    for i = 1:nPop
        % Update Velocity
        Particle(i).Velocity = w * Particle(i).Velocity + ...
            c1 * rand(VarSize) .* (Particle(i).Best.Position - Particle(i).Position)...
            + c2 * rand(VarSize) .* (GlobalBest.Position - Particle(i).Position);
        
        % Update Position
        Particle(i).Position = Particle(i).Position + Particle(i).Velocity;
        
        % Evlaute New Position
        Particle(i).Cost = CostFunction(Particle(i).Position(1),Particle(i).Position(2));
        
        % Compare New Position and Cost to all other Values in the System
       
        if Particle(i).Cost < Particle(i).Best.Cost
            Particle(i).Best.Position = Particle(i).Position;
            Particle(i).Best.Cost = Particle(i).Cost;
            
            if Particle(i).Best.Cost < GlobalBest.Cost
                GlobalBest = Particle(i).Best;
            end   
        end
    scatter(Particle(i).Position(1), Particle(i).Position(2), 50, 'k', 'filled')   %plot single particle to track over each generation
   
    
%     q = quiver(Particle(i).Position(1), Particle(i).Position(2), Particle(i).Velocity(1), Particle(i).Velocity(2), 'k');   %plot single particle to track over each generation
%     q.Marker = '.';
%     q.LineWidth = 2;
%     q.MarkerSize = 20;
%     q.MaxHeadSize = 30;
    pause(0.00005);
    end
   
    
    % Store the Best Cost Value at Every Iteration
    BestCosts(gen) = GlobalBest.Cost;
    
    %Display Iteration Information
    disp(['Iteration ' num2str(gen)  ':Best Cost = ' num2str(BestCosts(gen))]);
end
hold off

%% Results

figure;
plot(BestCosts, 'LineWidth', 2)
