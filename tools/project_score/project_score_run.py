from tools.project_score.Brand_Articles import Articles
from tools.project_score.Brand_Enterprise import Enterprise
from tools.project_score.Brand_IndexSpider import OutsideIndex
from tools.project_score.Brand_RoundAndAmount import RoundAndAmount
from tools.project_score.CommentsScore import CommentScore
from tools.project_score.ProjectInfoScore import ProjecctInfoScore
from tools.project_score.project_calc_last import LastScore

# ba = Articles()
# ba.NormalArticle()
# be = Enterprise()
# be.NormalFoundAndIndustry()
# bi = OutsideIndex()
# bi.NormalSpider()
# br = RoundAndAmount()
# br.NormalRoundAndAmount()
# cs = CommentScore()
# cs.NormalUserScore()
# pi = ProjecctInfoScore()
# pi.NormalProjectInfo()
pcl = LastScore()
pcl.getAllScore()
