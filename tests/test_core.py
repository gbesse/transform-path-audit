import unittest,math
from transform_path_audit import run

def edge(id,a,b,t,q=None,time=1):return dict(id=id,**{'from':a,'to':b},translation=t,q=q or [1,0,0,0],time=time)
def check(es,**kw):return run(dict(frames=['a','b','c'],reference='a',at=1,max_age=0,transforms=es,**kw))
class DomainTests(unittest.TestCase):
 def test_bad_cycle_witness(self):
  r=check([edge('ab','a','b',[1,0,0]),edge('bc','b','c',[0,1,0]),edge('ac','a','c',[1,2,0])]);self.assertFalse(r['consistent_current_component']);self.assertGreater(len(r['conflicts']),0)
 def test_inverse_rotation_and_translation(self):
  q=[math.sqrt(.5),0,0,math.sqrt(.5)];r=check([edge('ba','b','a',[1,0,0],q)]);t=r['transforms_from_reference']['b']['translation'];self.assertAlmostEqual(t[0],0);self.assertAlmostEqual(t[1],1)
 def test_sign_equivalent_quaternions(self):self.assertTrue(check([edge('ab','a','b',[1,0,0]),edge('ab2','a','b',[1,0,0],[-1,0,0,0])])['consistent_current_component'])
 def test_stale_edge_does_not_connect(self):
  r=check([edge('ab','a','b',[0,0,0],time=0)]);self.assertIn('b',r['unreachable_frames']);self.assertEqual(r['rejected_edges'][0]['reason'],'stale')
 def test_non_unit_quaternion(self):
  with self.assertRaises(ValueError):check([edge('ab','a','b',[0,0,0],[2,0,0,0])])
