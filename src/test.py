from api.new_v2board import NewV2board
from api.objects.user import User

a = NewV2board("inbound-name")
fu = User(22, "3b0fd577-4798-40ae-9473-58c5cf39ba63@mail.com", "dd2ea87f-c526-44f4-94fc-66db33ee2ed7")
a.get_users()
fu.set_usage(10000, 1073741824)
a.report_usage([])
