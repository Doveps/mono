from bassist.parser.log_file import debs_stdout, groups_stdout, shadow_stdout, users_stdout
import store_data

def record_base_flavors():
	for deb in debs_stdout.debs:
		store_data.store_debs(deb[0], deb[1], deb[2], deb[3])

	for group in groups_stdout.groups:
		store_data.store_groups(group[0], group[1], group[2], group[3])

	for shad in shadow_stdout.shadow:
		store_data.store_shadow(shad[0], shad[1], shad[2], shad[3], shad[4], shad[5], shad[6], shad[7], shad[8])

	for user in users_stdout.users:
		store_data.store_users(user[0], user[1], user[2], user[3], user[4], user[5], user[6])

def record_comparison_flavors():
	for deb in debs_stdout.debs:
		store_data.store_debs2(deb[0], deb[1], deb[2], deb[3])

	for group in groups_stdout.groups:
		store_data.store_groups2(group[0], group[1], group[2], group[3])

	for shad in shadow_stdout.shadow:
		store_data.store_shadow2(shad[0], shad[1], shad[2], shad[3], shad[4], shad[5], shad[6], shad[7], shad[8])

	for user in users_stdout.users:
		store_data.store_users2(user[0], user[1], user[2], user[3], user[4], user[5], user[6])