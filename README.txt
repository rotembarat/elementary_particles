-------------------------------------------------------------------

     =========================================================
       Geant3 Lab C TAU - Simulation of Elementary Particles
     =========================================================

                            -----------

 This python3 library allows the user to run a bulk of elementary particles,
 using the GEANT3 simulation provided for the Elementary Particles experiment
 in Lab C. The library has two operating modes - the first for the calibration
 of the detectors and the second for the calculation of mass and lifetime of
 pi-0 and kappa-short mesons. The modes differentiate by the data collected 
 and stored by the code. A code for lambda is not available at the moment 
 (March 9th 2020).

1- HOW TO RUN THE SIMULATION
   - Download and install Python3 before running the simulation.
   - Download all of the files and place them in a single directory.
   - Run the desired main code - clibration.py, part2_pi0.py or part2_kshort.py
     and follow the instructions in the relevant section below.
   - In case there is a required library missing, install it using pip:
     python3 -m pip install LIBRARY_NAME

2- CALIBRATION - calibration.py
   The code injects a praticle X times, as selected by the user. The user has 
   to insert:
   - TAU username and password
   - Particle name, as it appears in the simulation 
   - Minimal momentum (GeV/c) for the injected particle
   - Momentum interval
   - Amount of injections
   The code returns an .xlsx file containing the required fields for the 
   calibration.

3- ANALYSIS OF PI-0 - part2_pi0.py
   The code runs X injections of pi-0 of a desired momentum, as selected by the
   user. The user has to insert:
   - TAU username and password
   - Particle's momentum (GeV/c)
   - Amount of injections
   The code returns the relevant data for calculating the mass of the pi-0 meson,
   the amount of successful injections (see below) and the amount of decays 
   (interesting events). 
   The data is accumulated from events for which two pulses were detected in the 
   calorimeter and no trajectories were detected in the spectrometer.

4- ANALYSIS OF K-SHORT - part2_kshort.py
   The code runs X injections of k-short of a desired momentum, as selected by the
   user. The user has to insert:
   - TAU username and password
   - Particle's momentum (GeV/c)
   - Amount of injections
   The code returns the relevant data for calculating the mass and lifetime of the
   k-short meson, the amount of successful injections (see below) and the amount of 
   decays (interesting events). 
   The data is accumulated from events for which two trajectories with one vertex
   only were detected in the spectrometer.

5- KNOWN ISSUES
   - Sometimes, when a command is sent to the server it returns a null response.
     This issue occurs in the simulation GUI as well, and not only when accessed 
     remotely. The user recieves a feedback from the code of how many of the requested
     injections were successful (contained data).  
   - The code has an issue to connect to the simulation server via certain WiFi 
     networks, one of them being Free-Tau WiFi network. To fix the issue change 
     the WiFi - a mobile HotSpot and the eduroam network usually work.
   - The code doesn't change the seed of the simulation, so the same results are 
     obtained in each run. For example, if one runs 3 injections and then, in a 
     different run, runs 5 injections, the first three injections of the second run
     will be identical to the data accumulated in the first simulation. If one,
     for example, desires two distinct sets of 250 injections, one should run 500
     injections and cut the data in half.
    

       
