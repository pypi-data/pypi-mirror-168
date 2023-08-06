import open3d as o3d
import numpy as np
import copy
import math
from tqdm import tqdm

class scapula():
    def __init__(self, file_name):
        self.mesh = o3d.io.read_triangle_mesh(file_name)
        self.mesh.compute_vertex_normals()
        self.pcd = o3d.io.read_point_cloud(file_name)
        self.guide_mesh = 0

    def get_points(self, point_local):
        self.p1 = point_local[0]
        self.p2 = point_local[1]
        self.p3 = point_local[2]
    
    def select_points(self):
        def pick_points(pcd):
            vis = o3d.visualization.VisualizerWithEditing()
            vis.create_window()
            vis.add_geometry(pcd)
            vis.add_geometry(pcd)
            vis.run()
            vis.destroy_window()
            return vis.get_picked_points()
        
        value = self.pcd.points
        picked_id_pcd = pick_points(self.pcd)
        self.p1 = value[picked_id_pcd[0]]
        self.p2 = value[picked_id_pcd[1]]
        self.p3 = value[picked_id_pcd[2]]
        self.id = picked_id_pcd

    def computer_circle(self):
        def find_center(p1, p2, p3):
            x1 = p1[0];y1 = p1[1];z1 = p1[2]
            x2 = p2[0];y2 = p2[1];z2 = p2[2]
            x3 = p3[0];y3 = p3[1];z3 = p3[2]
            a1 = (y1*z2 - y2*z1 - y1*z3 + y3*z1 + y2*z3 - y3*z2)
            b1 = -(x1*z2 - x2*z1 - x1*z3 + x3*z1 + x2*z3 - x3*z2)
            c1 = (x1*y2 - x2*y1 - x1*y3 + x3*y1 + x2*y3 - x3*y2)
            d1 = -(x1*y2*z3 - x1*y3*z2 - x2*y1*z3 + x2*y3*z1 + x3*y1*z2 - x3*y2*z1)
            a2 = 2 * (x2 - x1)
            b2 = 2 * (y2 - y1)
            c2 = 2 * (z2 - z1)
            d2 = x1*x1 + y1*y1 + z1*z1 - x2*x2 - y2*y2 - z2*z2
            a3 = 2 * (x3 - x1)
            b3 = 2 * (y3 - y1)
            c3 = 2 * (z3 - z1)
            d3 = x1*x1 + y1*y1 + z1*z1 - x3*x3 - y3*y3 - z3*z3
            x = -(b1*c2*d3 - b1*c3*d2 - b2*c1*d3 + b2*c3*d1 + b3*c1*d2 - b3*c2*d1) / (a1*b2*c3 - a1*b3*c2 - a2*b1*c3 + a2*b3*c1 + a3*b1*c2 - a3*b2*c1)
            y = (a1*c2*d3 - a1*c3*d2 - a2*c1*d3 + a2*c3*d1 + a3*c1*d2 - a3*c2*d1) / (a1*b2*c3 - a1*b3*c2 - a2*b1*c3 + a2*b3*c1 + a3*b1*c2 - a3*b2*c1)
            z = -(a1*b2*d3 - a1*b3*d2 - a2*b1*d3 + a2*b3*d1 + a3*b1*d2 - a3*b2*d1) / (a1*b2*c3 - a1*b3*c2 - a2*b1*c3 + a2*b3*c1 + a3*b1*c2 - a3*b2*c1)
            return x, y, z

        p1 = self.p1; p2 = self.p2; p3 = self.p3
        x, y, z = find_center(p1, p2, p3)
        r_circle = np.sqrt((p1[0] - x)**2 + (p1[1] - y)**2 + (p1[2] - z)**2)
        
        self.center = [x, y, z]
        self.r = r_circle

    def move_center_to_O(self):
        def change_mesh(mesh_first, x, y, z):
            a = [-x, -y, -z]
            mesh_second = copy.deepcopy(mesh_first).translate(tuple(a))
            mesh_second.compute_vertex_normals()
            return mesh_second
        x = self.center[0]; y = self.center[1]; z = self.center[2]
        self.mesh = change_mesh(self.mesh, x, y, z)

    def find_vector(self):
        def find_normal_vector(p1, p2, p3):
            x1 = p1[0];y1 = p1[1];z1 = p1[2]
            x2 = p2[0];y2 = p2[1];z2 = p2[2]
            x3 = p3[0];y3 = p3[1];z3 = p3[2]
            a = (y2 - y1) * (z3 - z1) - (y3 - y1) * (z2 - z1)
            b = (z2 - z1) * (x3 - x1) - (z3 - z1) * (x2 - x1)
            c = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)
            return [a, b, c]

        def find_dis(point, mesh):
            mesh2 = copy.deepcopy(mesh)
            mesh2 = o3d.t.geometry.TriangleMesh.from_legacy(mesh)
            scene = o3d.t.geometry.RaycastingScene()
            _ = scene.add_triangles(mesh2)
            query_point = o3d.core.Tensor([point], dtype=o3d.core.Dtype.Float32)
            return scene.compute_signed_distance(query_point)

        def amount_point(normal_vector, mesh_second):
            length = 0.1
            j = 0
            for i in range(100):
                vector_point = normal_vector * (length * i)
                if find_dis(vector_point, mesh_second) < 0:
                    j = j + 1
            return j

        def dis(x, y):
            return np.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2 + (x[2] - y[2]) ** 2)

        def find_angle(p1, p2, p3):
            l1 = dis(p1, p2); l2 = dis(p2, p3); l3 = dis(p1, p3)
            cos = (l1 ** 2 + l2 ** 2 - l3 ** 2) / (2 * l1 * l2)
            return math.acos(cos)/np.pi

        def rotate_mesh(normal_vector):
            point_coordinate = [0, 0, 0]
            # 向量OB，也就是法向量
            vector_ob = [normal_vector[0], normal_vector[1], normal_vector[2]]

            # 法向量与z轴的夹角
            theta = find_angle(vector_ob, [0, 0, 0], [0, 0, 1])

            # 第一次旋转
            vector_ob2 = [0, np.sin(np.pi * theta), np.cos(np.pi * theta)]
            alpha = find_angle(vector_ob, [0, 0,np.cos(np.pi * theta)], vector_ob2)
            if vector_ob[0] < 0:
                alpha = - alpha
            
            R = self.mesh.get_rotation_matrix_from_xyz((0, 0, np.pi * alpha))
            mesh_third = copy.deepcopy(self.mesh)
            mesh_third.rotate(R, center=point_coordinate)

            # 第二次旋转
            R = self.mesh.get_rotation_matrix_from_xyz((np.pi * theta, 0, 0))
            mesh_fourth = copy.deepcopy(mesh_third)
            mesh_fourth.rotate(R, center=point_coordinate)
            return mesh_fourth

        def rotate_mesh2(normal_vector, mesh):
            point_coordinate = (0, 0, 0)
            # 向量OB，也就是法向量
            vector_ob = [normal_vector[0], normal_vector[1], normal_vector[2]]
            print (vector_ob)

            # 法向量与z轴的夹角
            mesh_second = copy.deepcopy(mesh)
            theta = find_angle(vector_ob, [0, 0, 0], [0, 1, 0])
            # print ('/n', theta, '/n'); print ('/n', find_angle(vector_ob, [0, 0, 0], [1, 0, 0]), '/n')
            R = mesh_second.get_rotation_matrix_from_xyz((0, 0, theta))
            mesh_third = copy.deepcopy(mesh)
            mesh_third.rotate(R, center=point_coordinate)
            return mesh_third

        def change_cylinder(mesh_cylinder1):
            point_coordinate = [0, 0, 0]
            a = - np.asarray(mesh_cylinder1.vertices)[0] + [0, 0, 0]
            mesh_cylinder2 = copy.deepcopy(mesh_cylinder1).translate(tuple(a))
            mesh_cylinder2.compute_vertex_normals()
            R = self.mesh.get_rotation_matrix_from_xyz((0, np.pi * 1, 0))
            mesh_cylinder = copy.deepcopy(mesh_cylinder2)
            mesh_cylinder.rotate(R, center=point_coordinate)
            return mesh_cylinder

        p1 = self.p1; p2 = self.p2; p3 = self.p3
        normal_vector_zero = find_normal_vector(p1, p2, p3)
        normal_vector_module = (normal_vector_zero[0] **2 + normal_vector_zero[1] **2 + normal_vector_zero[2] **2) **0.5
        normal_vector = (np.asarray(normal_vector_zero)) / normal_vector_module
        normal_vector_back = normal_vector * (-1)

        numeber =  amount_point(normal_vector, self.mesh)
        numeber_back = amount_point(normal_vector_back, self.mesh)
        if numeber_back > numeber:
            normal_vector = normal_vector_back

        self.mesh = rotate_mesh(normal_vector)
        # print (normal_vector)

        self.mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size = 100)
        self.mesh_frame.compute_vertex_normals()

        p1 = np.array(self.mesh.vertices[self.id[0]])
        vector2 = np.array(p1) / ((p1[0] **2 + p1[1] **2 + p1[2] **2) **0.5)
        self.mesh = rotate_mesh2(vector2, self.mesh)

        self.cylinder = o3d.geometry.TriangleMesh.create_cylinder(radius=3.25,
                                                          height=50)
        self.cylinder = change_cylinder(self.cylinder)

        self.mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size = 100)
        self.mesh_frame.compute_vertex_normals()

        # o3d.visualization.draw_geometries([self.cylinder, self.mesh, self.mesh_frame])

    def find_nail(self):
        def dis(x, y):
            return np.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2 + (x[2] - y[2]) ** 2)

        def find_dis2(point):
            # mesh = copy.deepcopy(mesh)
            query_point = o3d.core.Tensor([point], dtype=o3d.core.Dtype.Float32)
            return scene.compute_signed_distance(query_point)

        mesh = self.mesh; point_coordinate = (0, 0, 0)

        try:
            mesh2 = copy.deepcopy(self.mesh)
            mesh2 = o3d.t.geometry.TriangleMesh.from_legacy(self.mesh)
            scene = o3d.t.geometry.RaycastingScene()
            _ = scene.add_triangles(mesh2)
        except:
            print ('mesh2')
            return

        # 1.设定步长，角度1是1°，角度2是18°
        theta1 = 5/5; theta2 = 360/20

        # 2.初始化记录器
        location = [0, [], []] # 长度，点的位置，圆柱的位置

        # 3.开始穷举
        p = []
        for i in range(5):
            for j in range(20):
                p.append([i, j])
        
        for z in tqdm(p):
            i = z[0]; j = z[1]
                
                # 3.1.得出当前需要计算的圆柱位置，并将位于初始位置的圆柱旋转到那里
            theta_y = 10 + theta1 * i; theta_z = theta2 * j
            R = mesh.get_rotation_matrix_from_xyz((0, theta_y * np.pi / 180, 0))
            mesh_cylinderchange1 = copy.deepcopy(self.cylinder)
            mesh_cylinderchange1.rotate(R, center=point_coordinate)
            R = mesh.get_rotation_matrix_from_xyz((0, 0, theta_z * np.pi / 180))
            mesh_cylinderchange = copy.deepcopy(mesh_cylinderchange1)
            mesh_cylinderchange.rotate(R, center=point_coordinate)

                # 3.2.对当前圆柱位置进行判定，计算算法为：对于圆柱的每一个点，沿着x轴正负方向各走200个单位长度，如果有一侧全部在模型外侧，则这个点在模型外侧。找到在模型外侧且离圆心最近的钉子上的点。
            length = 0.1
            dis_origin = 100
            pcd2 = mesh_cylinderchange.sample_points_uniformly(number_of_points=200)
            point = np.asarray(pcd2.points)
            point_dis_coordinate = np.array([dis(point[k], point_coordinate) for k in range(200)])
                
            for k in range(200):
                if (point_dis_coordinate[k] >= dis_origin) or (point_dis_coordinate[k] <= 5):
                    continue

                judge1 = -1; judge2 = -1
                position_x = np.arange(0, 80, 0.1) + point[k][0]
                position_x = position_x.reshape(-1, 1)
                position_y = np.repeat(point[k][1], 800).reshape(-1, 1)
                position_z = np.repeat(point[k][2], 800).reshape(-1, 1)
                position = np.concatenate((position_x, position_y, position_z),axis=1)
                dis2 = find_dis2(position)
                dis2 = dis2.reshape(-1)
                if (dis2>=0).all():
                    judge1 = 1
                    
                position_x = np.arange(-80, 0, 0.1) + point[k][0]
                position_x = position_x.reshape(-1, 1)
                position_y = np.repeat(point[k][1], 800).reshape(-1, 1)
                position_z = np.repeat(point[k][2], 800).reshape(-1, 1)
                position = np.concatenate((position_x, position_y, position_z),axis=1)
                dis2 = find_dis2(position)
                dis2 = dis2.reshape(-1)
                if (dis2>=0).all():
                    judge2 = 1

                if (judge1 > 0 or judge2 > 0) and (dis_origin > point_dis_coordinate[k]):
                    dis_origin = point_dis_coordinate[k]
                    know = point[k]
                        
            if (dis_origin != 100) and (dis_origin > location[0]):
                location[0] = dis_origin; location[1] = know; location[2] = [i, j]
        self.location = location

        R = mesh.get_rotation_matrix_from_xyz((0, (5/5*location[2][0]+10)*np.pi / 180, 0))
        mesh_cylinderchange1 = copy.deepcopy(self.cylinder)
        mesh_cylinderchange1.rotate(R, center=point_coordinate)
        R = mesh.get_rotation_matrix_from_xyz((0, 0, (360/20)*location[2][1]*np.pi / 180))
        mesh_cylinderchange = copy.deepcopy(mesh_cylinderchange1)
        mesh_cylinderchange.rotate(R, center=point_coordinate)
        self.cylinder = copy.deepcopy(mesh_cylinderchange)

    def find_guide(self):
        mesh1 = o3d.t.geometry.TriangleMesh.from_legacy(self.mesh)
        scene = o3d.t.geometry.RaycastingScene()
        scene.add_triangles(mesh1)
        a=np.array([])
        r_circle = self.r
        r_circle /= 2 / 3

        p = []
        for i in range(180):
            for j in range(180):
                for k in range(15):
                    p.append([i, j, k])
        for z1 in tqdm(p):
            i = z1[0]; j = z1[1]; k = z1[2]
            x=(-r_circle / 2) + r_circle / 180 * i; y=(self.mesh.vertices[self.id[0]][1]) - r_circle / 180 * j; z = (-10) + 0.8 * k
            query_point = o3d.core.Tensor([[x,y,z]],dtype=o3d.core.Dtype.Float32)
            ans = scene.compute_closest_points(query_point)
            points=ans['points'].numpy()
            triangle=ans['primitive_ids'][0].item()
            a=np.append(a,triangle)
            a=a.astype(int)

        mesh2 = copy.deepcopy(self.mesh)
        mesh2.triangles = o3d.utility.Vector3iVector(
        np.asarray(mesh2.triangles)[a])
        mesh2.triangle_normals = o3d.utility.Vector3dVector(
        np.asarray(mesh2.triangle_normals)[a])
        mesh2.paint_uniform_color([0.1, 0.1, 0.7])

        mesh2.compute_vertex_normals()
        pcd1 = mesh2.sample_points_uniformly(number_of_points=10000)

        xyz= np.asarray(pcd1.points)
        p = []
        z1 = []
        for i in range(10000):
            for j in range(5):
                z1.append([i, j])
        for z in tqdm(z1):
            i = z[0]; j = z[1]
            q = [xyz[i, 0], xyz[i, 1], xyz[i, 2] - j * 0.5]
            p.append(q)
        p = np.array(p)
        pcd2 = o3d.geometry.PointCloud()
        pcd2.points = o3d.utility.Vector3dVector(p)
        self.guide_pcd = pcd2
    
    def pcd_2_mesh(self, pcd2):

        '''radius = 0.01  # 搜索半径
        max_nn = 30  # 邻域内用于估算法线的最大点数
        pcd2.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius, max_nn))'''

        mesh4 = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd2, alpha=2)
        mesh4.compute_vertex_normals()
        mesh4.paint_uniform_color([0, 0.8,0.8])
        return mesh4
    
    def show(self, l):
        o3d.visualization.draw_geometries(l)