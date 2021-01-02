list = ['cse','ece','civil','mech','meta','chem','eee','bio','mtech-cse-csis','mtech-cse-cse','c_est','c_wre','c_rsg','c_ctm','c_te','c_gte','c_ese','mtech-eee-pse','mtech-eee-ped','mtech-mech-te','mtech-mech-cim','mtech-mech-ae','mtech-mech-msed','mtech-mech-me','mtech-mech-md','mtech-mech-am','mtech-ece-ei','mtech-ece-acm','mtech-ece-vlsi','mtech-mme-im','mtech-mme-mt','mtech-che-ce','mtech-che-pc','mba-operations','mba-marketing','mba-hr','mba-finance','msct-p','msct-e','msct-i','mscm-am','mscm-msc','mscc-oc','mscc-mmc','phd-ce','phd-me','phd-ee','phd-ece','phd-mme','phd-cse','phd-bt','phd-maths','phd-phy','phd-che','phd-hss','phd-som']

sql = ""

for l in list :
    sql += "INSERT INTO `administrator_branch` (`id`, `branch`, `branchCode`, `course_id`) VALUES (NULL, '"+l+"', '"+l+"', 'dummy');"

print(sql)