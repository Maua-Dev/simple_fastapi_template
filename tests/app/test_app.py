from src.app.main import read_root, get_history, withdraw, deposit


class Test_App:
    def test_read_root(self):
        resp = read_root()

        assert resp == {
            "name": "Luigi Trevisan",
            "agency": "0000",
            "account": "00000-0",
            "current_balance": 1000.0
        }

    def test_get_history(self):
        resp = get_history()

        assert resp == {
            'all_transactions' : [
                {
                    "type" : "deposit",
                    "value" : 100.0,
                    "timestamp" : 1690482853890
                },
                {
                    "type" : "withdraw",
                    "value" : 200.0,
                    "timestamp" : 1690482853890
                }
            ]
        }
        
    def test_withdraw(self):
        resp = withdraw({
            "200": 1,
            "100": 1,
            "50": 1,
            "20": 1,
            "10": 1,
            "5": 1,
            "2": 1
        })

        assert resp == {
            "current_balance": 1000.0,
            "timestamp": 1690482853890, #milliseconds
        }
        
    def test_deposit(self):
        resp = deposit({
            "200": 1,
            "100": 1,
            "50": 1,
            "20": 1,
            "10": 1,
            "5": 1,
            "2": 1
        })

        assert resp == {
            "current_balance": 1000.0,
            "timestamp": 1690482853890, #milliseconds
        }