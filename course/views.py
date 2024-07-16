from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly,AllowAny
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import (Course, Lesson, Comment, Category,
                     LearningPath, Enrollment, Module, Progress
                     )
from .serializers import (LearningPathSerializer, CategorySerializer, CourseSerializer,
                          CourseStatusSerializer, CourseDetailSerializer, ModuleSerializer,
                            CourseDetailStatusSerializer, LessonSerializer, CommentSerializer,
                             EnrollmentSerializer, ProgressSerializer)

class LearningPathListAPIView(APIView):
    def get(self, request):
        try:
            learning_paths = LearningPath.objects.all()
            serializer = LearningPathSerializer(learning_paths, many=True)

            return Response({'data':serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
    def post(self, request):
        data = request.data
        try:
            learning_Path = LearningPath.objects.create(
                title = data.get('title'),
                description = data.get('description')
            )
            learning_Path.save()
            serializer = LearningPathSerializer(learning_Path, many=False)

            return Response({'data':serializer.data},status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
class LearningPathAPIView(APIView):
    def get(self, request, lp_slug):
        try:
            learning_paths = LearningPath.objects.get(slug=lp_slug)
            serializer = LearningPathSerializer(learning_paths, many=False)

            return Response({'data':serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,lp_slug):
        data = request.data
        try:
            learning_Path = LearningPath.objects.get(slug=lp_slug)
            learning_Path.title = data.get('title')
            learning_Path.description = data.get('description')
            learning_Path.save()
            serializer = LearningPathSerializer(learning_Path, many=False)

            return Response({'data':serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,lp_slug):
        try:
            learning_path = LearningPath.objects.get(slug=lp_slug)
            learning_path.delete()

            return Response(
                {"data": f" The Learning Path {learning_path.title} has been deleted successfully"}
                ,status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CategoryListAPIView(APIView):
    def get(self, request):
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)

            return Response({'data':serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data
        try:
            category = Category.objects.create(
                title = data.get('title'),
                description = data.get('description')
            )
            category.save()
            serializer = CategorySerializer(category, many=False)

            return Response({'data':serializer.data},status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
class CategoryAPIView(APIView):
    def get(self, request, cat_slug):
        try:
            category = Category.objects.get(slug=cat_slug)
            serializer = CategorySerializer(category, many=False)

            return Response({'data':serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,cat_slug):
        data = request.data
        try:
            category = Category.objects.get(slug=cat_slug)
            category.title = data.get('title')
            category.description = data.get('description')
            category.save()
            serializer = CategorySerializer(category, many=False)

            return Response({'data':serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,cat_slug):
        try:
            category = Category.objects.get(slug=cat_slug)
            category.delete()

            return Response(
                {"data": f" The Category {category.title}  has been deleted successfully"}
                ,status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CoursesListAPIView(ListAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            lp_slug = self.request.query_params.get('lp_slug')
            cat_slug = self.request.query_params.get('cat_slug')

            if lp_slug:
                queryset = self.filter_by_learning_path(lp_slug)
            elif cat_slug:
                queryset = self.filter_by_category(cat_slug)
            else:
                queryset = self.get_queryset()

            serializer = self.get_serializer(queryset, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def filter_by_learning_path(self, lp_slug):
        courses = Course.objects.filter(learning_path__slug=lp_slug)
        return courses

    def filter_by_category(self, cat_slug):
        courses = Course.objects.filter(categories__slug=cat_slug)
        return courses

    def post(self, request):
        data = request.data
        try:
            course = Course.objects.create(
                title = data.get('title'),
                status=data.get('status'),
                created_by=request.user,
                short_description = data.get('short_description'),
                long_description = data.get('long_description')
            )
            # Handle categories
            category_ids = data.getlist('categories[]')
            for category_id in category_ids:
                category = Category.objects.get(id=category_id)
                course.categories.add(category)
                # print("For Category")
                # print(category)
                # print(course)
            
            # Handle learning path
            learning_path_id = data.get('learning_path')
            if learning_path_id:
                learning_path = LearningPath.objects.get(id=learning_path_id)
                course.learning_path = learning_path
                # print("For Learning Path")
                # print(learning_path)
                # print(course)
            image_file = data.get('image')
            if image_file:
                course.image.save(image_file.name, image_file)
            course.save()
            serializer = CourseDetailSerializer(course, many=False)

            return Response({'data':serializer.data},status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
class CoursesAPIView(APIView):
    def get(self, request, course_slug):
        try:
            course = Course.objects.get(slug=course_slug)
            serializer = CourseDetailSerializer(course, many=False)

            return Response({'data':serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,course_slug):
        data = request.data
        try:
            course = Course.objects.get(slug=course_slug, created_by=request.user)
            course.title = data.get('title')
            course.long_description = data.get('long_description')
            course.short_description = data.get('short_description')
            course.status=data.get('status')

            if 'categories' in data:
                category_ids = data['categories']
                categories = Category.objects.filter(id__in=category_ids)
                course.categories.set(categories)

            image_file = data.get('image')
            if image_file:
                course.image.save(image_file.name, image_file)           
            course.save()
            serializer = CourseDetailSerializer(course, many=False)

            return Response({'data':serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,course_slug):
        try:
            course = Course.objects.get(slug=course_slug, created_by=request.user)
            course.delete()

            return Response(
                {"data": f" The Course {course.title}  has been deleted successfully"}
                ,status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ModuleListAPiView(APIView):
    def get(self, request, course_slug):
        try:
            modules = Module.objects.filter(course__slug=course_slug)
            serializer = ModuleSerializer(modules, many=True)

            return Response({'data':serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, course_slug):
        data = request.data
        try:
            course = Course.objects.get(slug=course_slug)
            module = Module.objects.create(
                course = course,
                title = data.get('title'),
                description = data.get('description'),
                is_open = data.get('is_open')
            )
            module.save()
            serializer = ModuleSerializer(module, many=False)

            return Response({'data':serializer.data},status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CourseStatusAPIView(APIView):
    def get(self, request, course_slug):
        try:
            course = Course.objects.get(slug=course_slug)
            serializer = CourseDetailStatusSerializer(course, many=False)

            return Response({'data':serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class CourseNoAuthAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, course_slug):
        try:
            course = Course.objects.get(slug=course_slug)
            serializer = CourseDetailSerializer(course, many=False)

            return Response({'data':serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class  ModuleAPiView(APIView):
    def get(self, request, course_slug, mod_slug):
        try:
            module = Module.objects.get(course__slug=course_slug, slug=mod_slug)
            serializer = ModuleSerializer(module, many=False)

            return Response({'data':serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request, course_slug, mod_slug):
        data = request.data
        try:
            module = Module.objects.get(course__slug=course_slug, slug=mod_slug)
            module.title = data.get('title')
            module.description = data.get('description')
            module.is_open = data.get('is_open')
            module.save()
            serializer = ModuleSerializer(module, many=False)

            return Response({'data':serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request, course_slug, mod_slug):
        try:
            module = Module.objects.get(course__slug=course_slug, slug=mod_slug)
            module.delete()

            return Response(
                {"data": f" The Module {module.title}  has been deleted successfully"}
                ,status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LessonListAPIView(APIView):
    def get(self, request, course_slug, mod_slug):
        try:
            lessons = Lesson.objects.filter(module__slug=mod_slug)
            serializer = LessonSerializer(lessons, many=True)

            return Response({'data':serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, course_slug, mod_slug):
        data = request.data
        try:
            lesson_type = data.get('lesson_type')
            module = Module.objects.get(slug=mod_slug)
            if lesson_type in ['article', 'video', 'file', 'quiz']:
                lesson_data = {
                    'module': module,
                    'title': data.get('title'),
                    'short_description':data.get('short_description'),
                    'status': data.get('status'),
                }

                if lesson_type == 'article':
                    lesson_data['lesson_type'] = 'article'
                    lesson_data['long_description'] = data.get('long_description')
                elif lesson_type == 'video':
                    lesson_data['lesson_type'] = 'video'
                    video_file = data.get('video')
                    if video_file:
                        lesson_data['video'] = video_file
                    else:
                        lesson_data['youtube_id'] = data.get('youtube_id')
                elif lesson_type == 'file':
                    lesson_data['lesson_type'] = 'file'
                    document_file = request.data.get('document')
                    if document_file:
                        lesson_data['file'] = document_file
                elif lesson_type == 'quiz':
                    pass

                lesson = Lesson.objects.create(**lesson_data)

                serializer = LessonSerializer(lesson, many=False)

                return Response({'data':serializer.data},status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Invalid lesson type.'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LessonAPIView(APIView):
    def get(self, request, course_slug, mod_slug,lesson_slug):
        try:
            lesson = Lesson.objects.get(module__slug=mod_slug, slug=lesson_slug)
            serializer = LessonSerializer(lesson, many=False)

            return Response({'data':serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request, course_slug, mod_slug,lesson_slug):
        data = request.data
        try:
            lesson_type = data.get('lesson_type')
            lesson = Lesson.objects.get(module__slug=mod_slug, slug=lesson_slug)
            lesson.title = data.get('title')
            lesson.short_description = data.get('short_description')
            lesson.status = data.get('status')
            if lesson_type == 'article':
                lesson.lesson_type = 'article'
                lesson.long_description = data.get('long_description')
            elif lesson_type == 'video':
                lesson.lesson_type = 'video'
                video_file = data.get('video')
                if video_file:
                    lesson.video = video_file
                else:
                    lesson.youtube_id = data.get('youtube_id')
            elif lesson_type == 'file':
                lesson.lesson_type = 'file'
                document_file = request.data.get('document')
                if document_file:
                    lesson.file = document_file
            elif lesson_type == 'quiz':
                pass
            lesson.save()
            serializer = LessonSerializer(lesson, many=False)

            return Response({'data':serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request, course_slug, mod_slug,lesson_slug):
        try:
            lesson = Lesson.objects.get(module__slug=mod_slug, slug=lesson_slug)
            lesson.delete()

            return Response(
                {"data": f" The Lesson {lesson.title}  has been deleted successfully"}
                ,status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CommentListAPIView(APIView):
    def get(self, request, course_slug, mod_slug, lesson_slug):
        try:
            comments = Comment.objects.filter(lesson__slug=lesson_slug)
            serializer = CommentSerializer(comments, many=True)

            return Response({'data':serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, course_slug, mod_slug, lesson_slug):
        data = request.data
        try:
            lesson = Lesson.objects.get(slug=lesson_slug, module__slug=mod_slug)
            comment = Comment.objects.create(
                lesson = lesson,
                title = data.get('title'),
                content = data.get('content'),
                created_by = request.user
            )
            comment.save()
            serializer = CommentSerializer(comment, many=False)

            return Response({'data':serializer.data},status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CommentAPIView(APIView):
    def get(self, request, course_slug, mod_slug, lesson_slug, pk=None):
        try:
            comment = Comment.objects.get(pk=pk,lesson__slug=lesson_slug)
            serializer = CommentSerializer(comment, many=False)

            return Response({'data':serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, course_slug, mod_slug, lesson_slug, pk=None):
        data = request.data
        try:
            comment = Comment.objects.get(pk=pk,lesson__slug=lesson_slug, created_by=request.user)
            comment.title = data.get('title')
            comment.content = data.get('content')
            comment.save()
            serializer = CommentSerializer(comment, many=False)

            return Response({'data':serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, course_slug, mod_slug, lesson_slug, pk=None):
        try:
            comment = Comment.objects.get(pk=pk,lesson__slug=lesson_slug, created_by=request.user)
            comment.delete()

            return Response(
                {"data": f" The Comment {comment.title}  has been deleted successfully"}
                ,status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class EnrollmentListAPIView(APIView):
    def get(self, request, course_slug):
        try:
            enrollments = Enrollment.objects.filter(course__slug=course_slug)
            serializer = EnrollmentSerializer(enrollments, many=True)

            return Response({'data':serializer.data,},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, course_slug):
        try:
            course = Course.objects.get(slug=course_slug)
            enrollment = Enrollment.objects.create(
                course = course,
                user = request.user
            )
            enrollment.save()
            serializer = EnrollmentSerializer(enrollment, many=False)

            return Response({'data':serializer.data},status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class EnrollmentAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, course_slug, pk=None):
        try:
            enrollment = Enrollment.objects.get(pk=pk,course__slug=course_slug)
            serializer = EnrollmentSerializer(enrollment, many=False)

            return Response({'data':serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProgressListAPIView(APIView):
    def get(self, request, course_slug):
        try:
            progress = Progress.objects.filter(course__slug=course_slug)
            serializer = ProgressSerializer(progress, many=True)

            return Response({'data':serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)