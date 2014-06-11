'''
Runner
'''
import test_case as TC
def main(inf_file,marker,plans):
    land = TC.factory_landscape(inf_file,calculation_now=False)

    clan_agile = TC.factory_agile_clan(land,plans)
    clan_agile.uncertainty_base = 0.0
    TC.run_simulation(clan_agile,20,TC.AdapterBehaviorAgileTeam,'test_agile_0_%s'%marker)
    print "------------------------"
    clan_agile = TC.factory_agile_clan(land,plans)
    clan_agile.uncertainty_base = 0.1
    TC.run_simulation(clan_agile,20,TC.AdapterBehaviorAgileTeam,'test_agile_1_%s'%marker)
    print "------------------------"
    clan_agile = TC.factory_agile_clan(land,plans)
    clan_agile.uncertainty_base = 0.5
    TC.run_simulation(clan_agile,20,TC.AdapterBehaviorAgileTeam,'test_agile_2_%s'%marker)
    print "------------------------"
    clan_water = TC.factory_wf_clan(land,plans)
    clan_water.uncertainty_base = 0.0
    TC.run_simulation(clan_water,20,TC.AdapterBehaviorWaterfallTeam,'test_water_0_%s'%marker)
    print "------------------------"
    clan_water = TC.factory_wf_clan(land,plans)
    clan_water.uncertainty_base = 0.1
    TC.run_simulation(clan_water,20,TC.AdapterBehaviorWaterfallTeam,'test_water_1%s'%marker)
    print "------------------------"
    clan_water = TC.factory_wf_clan(land,plans)
    clan_water.uncertainty_base = 0.5
    TC.run_simulation(clan_water,20,TC.AdapterBehaviorWaterfallTeam,'test_water_2%s'%marker)
    print "------------------------"

if __name__ == "__main__":
    plans = [[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]]
    # plans = [[0,1,2,3,4,5]]
    print "================="
    main("inf/n16k0.txt","n16k0",plans)
    # print "================="
    # main("inf/n16k8.txt","n16k8",plans)
    # print "================="
    # main("inf/n16k15.txt","n16k15",plans)