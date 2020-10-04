
from business_plan import Bot, License, PackageLicense, Customer, Company, \
    BusinessPlanOptimizer

license_analysis = License(80*12, analysis_license=True)
license_engineer = License(400*12, engineer_license=True)
license_sdk = License(2000*12, sdk_license=True)

pk_dev = PackageLicense(licenses=[license_analysis]*20+[license_engineer]*5+[license_sdk]*1)
pk_no_dev = PackageLicense(licenses=[license_analysis]*20+[license_engineer]*5)

bot_customer = Bot(rent_library=15e3,package_license=pk_dev,
                   develop_by_customer=True, discount=0.4)
bot_esn = Bot(rent_library=15e3,package_license=pk_dev,
              develop_by_esn=True, discount=0.4)

bot_dessia = Bot(rent_library=40e3,package_license=pk_no_dev,
                 develop_by_dessia=True, discount=0.4)

large_compagny = Company(large_company=True)
middle_compagny = Company(middle_company=True)
small_compagny = Company(small_company=True)

c1 = Customer(bots=[bot_dessia]*3+[bot_customer]*2, company=large_compagny)

opt1 = BusinessPlanOptimizer(number_bots=[[5, 5], [10, 25], [50, 100], [100, 250], [300, 400]],
                             dessia_bot_ratio=[[1, 1], [0.6, 0.8], [0.6, 0.8], [0.3, 0.5], [0.2, 0.4]],
                             revenue=[[200e3, 200e3], [800e3, 800e3], [1500e3, 2500e3], [2500e3, 4000e3], [5000e3, 8000e3]],
                             discount_range=[[0.5, 0.8], [0.5, 0.8], [0.5, 0.8], [0.3, 0.8], [0.3, 0.8]],
                             )
