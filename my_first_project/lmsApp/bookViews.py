from django.shortcuts import render,redirect
from django.utils import timezone
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from rest_framework.exceptions import NotFound
from .models import Book,Member,LoanRequest
from django.db.models import Q
from .serrializer import BookSerializer,LoanSerializer
from .form import BookForm

# Create your views here.
# def home(request):
#     return render(request,'lmsApp/home.html')

@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer,JSONRenderer])
def book_list(request):
    books=Book.objects.all()
    # Track books with active/pending requests for the current member (temporary fallback).
    member = Member.objects.first()
    applied_book_ids = []
    
    if member:
        # Find books where the member has a pending request or an active loan
        active_requests = LoanRequest.objects.filter(
            member=member
        ).filter(
            Q(status='PENDING') | 
            (Q(status='APPROVED') & Q(loan__return_date__isnull=True))
        ).values_list('book_id', flat=True)
        
        applied_book_ids = list(active_requests)

    serializer=BookSerializer(books,many=True)

    if request.accepted_renderer.format=="json":
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    return Response(
        {'books': books, 'applied_book_ids': applied_book_ids},
        template_name='lmsApp/book pages/book_list.html'
    )
    
@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer,JSONRenderer])
def book_details(request,book_id):
    try:
        book=Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise NotFound("Book Not Found")
    
    serializer=BookSerializer(book)

    if request.accepted_renderer.format=="json":
        return Response(serializer.data)
    
    return Response(
        {'book':book},
        template_name='lmsApp/book pages/book_detail.html'
    )

@api_view(['POST','GET'])
@renderer_classes([TemplateHTMLRenderer,JSONRenderer])
def AddBook(request):
    if request.method=="POST":
        if request.accepted_renderer.format=="html":
            form=BookForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('book_list')
            else:
                return Response({'form':form},template_name="lmsApp/book pages/book_form.html",status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer=BookSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {'data':serializer.data},status=status.HTTP_201_CREATED,
            )
    else:
        if request.accepted_renderer.format=="html":
            form=BookForm()
            return Response({'form':form},template_name='lmsApp/book pages/book_form.html')
        
        serializer=BookSerializer()
        return Response(serializer.data)

@api_view(['PATCH','PUT','POST','GET'])
@renderer_classes([TemplateHTMLRenderer,JSONRenderer])
def UpdateBook(request,book_id):
    try:
        book=Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise NotFound("Book Not Found")
    
    if request.method in ["PUT","POST"]:
        if request.accepted_renderer.format=="html":
            form=BookForm(request.POST,instance=book)
            if form.is_valid():
                form.save()
                return redirect('book_list')
            else:
                return Response({'form':form},template_name='lmsApp/book pages/book_form.html',status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer=BookSerializer(book,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'data':serializer.data},status=status.HTTP_200_OK)
    
    elif request.method=="PATCH":
        if request.accepted_renderer.format=="html":
            form=BookForm(request.POST,instance=book)
            if form.is_valid():
                form.save()
                return redirect('book_list')
            else:
                return Response({'form':form},template_name='lmsApp/book pages/book_form.html',status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer=BookSerializer(book,data=request.data,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'data':serializer.data},status=status.HTTP_200_OK)
    else:
        if request.accepted_renderer.format=="html":
            form=BookForm(instance=book)
            return Response({'form':form},template_name="lmsApp/book pages/book_form.html")
        serializer=BookSerializer(book)
        return Response(serializer.data)

@api_view(['DELETE','GET','POST'])
@renderer_classes([TemplateHTMLRenderer,JSONRenderer])
def DeleteBook(request,book_id):
    try:
        book=Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise NotFound("Book Not Found")
    
    if request.method=="DELETE":
        book.delete()
        
        if request.accepted_renderer.format=="html":
            return redirect('book_list')
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    if request.method=="POST":
        book.delete()
        
        if request.accepted_renderer.format=="html":
            return redirect('book_list')
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    if request.accepted_renderer.format=="html":
        return Response(
            {'book': book},
            template_name="lmsApp/book pages/confrim_delete.html"
        )

    serializer=BookSerializer(book)
    return Response(serializer.data,status=status.HTTP_200_OK)


class loanMgtView(APIView):
   
    def post(self,request,book_id,member_id):

        try:
            book=Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({"error":"Book not found"},status=status.HTTP_404_NOT_FOUND)
        
        try:
            member=Member.objects.get(pk=member_id)
        except Member.DoesNotExist:
            return Response({"error":"Member not found"},status=status.HTTP_404_NOT_FOUND)
        
        today=timezone.now().date()

        # Block new loans if any active loans are overdue.
        active_loans=member.loans.filter(return_date__isnull=True)
        overdue_loans=[loan for loan in active_loans if loan.is_overdue]

        if overdue_loans:
            return Response({"error":"Member has overdue loans. Can not issue new book."},status=status.HTTP_400_BAD_REQUEST)
        
        if book.available_copies <= 0:
            return Response({"error":"No available copies for this book."},status=status.HTTP_400_BAD_REQUEST)
        
       
        serializer=LoanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(book=book,member=member,return_date=today+timezone.timedelta(days=7))
        return Response(serializer.data,status=status.HTTP_201_CREATED)

