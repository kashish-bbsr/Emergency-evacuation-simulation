from simulation import Simulation

if __name__ == "__main__":
    sim = Simulation(width=50, height=50, num_agents=30)
    sim.env.load_shelters("data/Shelter_Data.csv")
    sim.env.load_transport_hazards("data/Transport_Data.csv")
    sim.env.load_hospitals("data/Hospital_Data.csv")
   #sim.env.load_density_map("data/Warehouse_Data.csv")  # Optional: treat warehouse as density zones
    #sim.load_agents_from_csv("data/Hospital_Data.csv")   # Optional: use hospital positions as agent start
    sim.run(steps=120)
    sim.save_video("evacuation.gif")