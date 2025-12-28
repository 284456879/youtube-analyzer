import unittest
import json
from app import app, db, GameRecord

class TestCase(unittest.TestCase):
    def setUp(self):
        # 使用内存数据库进行测试，不影响实际数据
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_page(self):
        """测试首页能否正常访问"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # 检查页面中是否包含我们写的标题 (注意中文编码)
        self.assertIn('专注力大冒险'.encode('utf-8'), response.data)
        print("✅ 首页访问测试通过")

    def test_api_record_flow(self):
        """测试成绩保存和读取流程"""
        # 1. 初始状态应该有3个占位符记录 (3, 4, 5 难度)
        response = self.client.get('/api/records')
        self.assertEqual(response.status_code, 200)
        records = json.loads(response.data)
        self.assertEqual(len(records), 3)
        self.assertEqual(records[0]['player_name'], '---')

        # 2. 模拟保存一个成绩 (难度3)
        data = {
            'game_type': 'schulte',
            'player_name': 'TestUser',
            'difficulty': '3',
            'score': 10.5,
            'accuracy': 100.0
        }
        response = self.client.post('/api/record', json=data)
        self.assertEqual(response.status_code, 201)
        
        # 3. 再次查询，难度3的记录应该更新了
        response = self.client.get('/api/records')
        records = json.loads(response.data)
        
        # 找到难度3的记录
        level_3_record = next(r for r in records if r['difficulty'] == '3')
        self.assertEqual(level_3_record['player_name'], 'TestUser')
        self.assertEqual(level_3_record['score'], 10.5)
        
        # 难度4的记录应该还是空的
        level_4_record = next(r for r in records if r['difficulty'] == '4')
        self.assertEqual(level_4_record['player_name'], '---')
        
        print("✅ API 数据存取测试通过")

    def test_leaderboard_logic(self):
        """测试排行榜逻辑：只保留最好成绩"""
        # 1. 用户A 创造记录 20s
        self.client.post('/api/record', json={
            'game_type': 'schulte', 'player_name': 'UserA', 'difficulty': '3', 'score': 20.0
        })
        
        # 2. 用户B 创造更好记录 15s
        self.client.post('/api/record', json={
            'game_type': 'schulte', 'player_name': 'UserB', 'difficulty': '3', 'score': 15.0
        })

        # 3. 查询，应该显示 UserB
        response = self.client.get('/api/records')
        records = json.loads(response.data)
        level_3_record = next(r for r in records if r['difficulty'] == '3')
        self.assertEqual(level_3_record['player_name'], 'UserB')
        self.assertEqual(level_3_record['score'], 15.0)
        
        print("✅ 排行榜逻辑测试通过")

if __name__ == '__main__':
    unittest.main()
