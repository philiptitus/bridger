from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from base.models import *
from base.serializers import *
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination



class IncomeCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()

        # Auto-set date_received to current date if not provided
        if 'date_received' not in data or not data['date_received']:
            data['date_received'] = timezone.now().date()

        # Check if the amount is within the specified range
        amount = data.get('amount')
        if amount is not None:
            try:
                amount = float(amount)
            except ValueError:
                return Response({'detail': 'Enter a valid amount.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if not (1000 <= amount <= 1000000000):
                return Response({'detail': 'Enter an amount in the range of 1000 and 1 billion.'}, status=status.HTTP_400_BAD_REQUEST)

        # Set the user to the request.user
        data['user'] = request.user.id

        serializer = IncomeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from django.db.models import Q, F


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Q


class UserIncomeListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IncomeSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        name = self.request.query_params.get('name')
        incomes = Income.objects.filter(user=self.request.user)
        if name:
            incomes = incomes.filter(Q(source__icontains=name) | Q(description__icontains=name))
        return incomes

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)







class UserIncomeUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            income = Income.objects.get(id=pk)
        except Income.DoesNotExist:
            return Response({'detail': 'Income Entry Not Found.'}, status=status.HTTP_400_BAD_REQUEST)

        if income.user != self.request.user:
            return Response({'detail': 'Access Denied !.'}, status=status.HTTP_400_BAD_REQUEST)

        return income

    def put(self, request, pk):
        income = self.get_object(pk)
        data = request.data.copy()
        
        # Check if the amount is within the specified range
        amount = data.get('amount')
        if amount is not None:
            try:
                amount = float(amount)
            except ValueError:
                return Response({'detail': 'Enter a valid amount.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if not (1000 <= amount <= 1000000000):
                return Response({'detail': 'Enter an amount in the range of 1000 and 1 billion.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = IncomeSerializer(income, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, NotFound

class UserIncomeDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            income = Income.objects.get(id=pk)
        except Income.DoesNotExist:
            return Response({'detail': 'Not Found.'}, status=status.HTTP_400_BAD_REQUEST)

        if income.user != self.request.user:
            return Response({'detail': 'Access Denied.'}, status=status.HTTP_400_BAD_REQUEST)

        return income

    def delete(self, request, pk):
        income = get_object_or_404(Income, id=pk)
        
        if income.user == self.request.user:
            income.delete()
  
            return Response({'detail': 'Deleted successfully.'}, status=status.HTTP_400_BAD_REQUEST)
        else:

            return Response({'detail': 'Access Denied.'}, status=status.HTTP_400_BAD_REQUEST)








from datetime import date

class BudgetCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        
        # Automatically set the start_date to today's date
        data['start_date'] = date.today()
        
        # Get the income ID from the request data
        income_id = data.get('income')
        
        try:
            income = Income.objects.get(id=income_id)
            
            # Check if the income entry is already associated with a budget
            if Budget.objects.filter(income=income).exists():
                return Response({'detail': 'This income entry is already associated with a budget.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Ensure the income entry belongs to the current user
            if income.user != request.user:
                return Response({'detail': 'You do not have permission to use this income entry.'}, status=status.HTTP_403_FORBIDDEN)
            
            # Automatically set the total_expenses to the income amount
            data['total_expenses'] = income.amount
        except Income.DoesNotExist:
            return Response({'detail': 'Income entry not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = BudgetSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









class BudgetDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        try:
            budget = Budget.objects.get(pk=pk)
        except Budget.DoesNotExist:
            return Response({'detail': 'Budget not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        income = budget.income
        if income.user != request.user:
            return Response({'detail': 'You do not have permission to delete this budget.'}, status=status.HTTP_403_FORBIDDEN)
        
        budget.delete()
        return Response({'detail': 'Budget deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)





# from django.conf import settings
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from datetime import date
# from decimal import Decimal, InvalidOperation
# import google.generativeai as genai
# import os
# import re
# import decimal

# class CategoryCreateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         genai.configure(api_key=settings.GOOGLE_API_KEY)

#     def post(self, request, *args, **kwargs):
#         budget_id = request.data.get('budget')
#         description = request.data.get('description')

#         if not budget_id or not description:
#             return Response({'detail': 'Budget and description are required.'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             budget = Budget.objects.get(id=budget_id)
#         except Budget.DoesNotExist:
#             return Response({'detail': 'Budget not found.'}, status=status.HTTP_404_NOT_FOUND)

#         if budget.income.user != request.user:
#             return Response({'detail': 'You do not have permission to create categories for this budget.'}, status=status.HTTP_403_FORBIDDEN)

#         # Fetch existing categories
#         existing_categories = Category.objects.filter(budget=budget)
#         existing_categories_text = "\n".join([f"{cat.name}: {cat.amount}" for cat in existing_categories])

#         model = genai.GenerativeModel('gemini-1.0-pro-latest')
#         prompt = f"""Update the following budget categories based on the description: '{description}'. 
#         Do not generate new categories unless explicitly specified. 
#         Ensure the total amount does not exceed {budget.total_expenses}. 
#         Existing categories and amounts are:
#         {existing_categories_text}
#         Return the data in the following format:
#         Category1: Amount1
#         Category2: Amount2
#         ...
#         CategoryN: AmountN
#         """
#         response = model.generate_content(prompt)

#         # Extract the text part of the response
#         if not hasattr(response, '_result'):
#             return Response({'detail': 'Error parsing Gemini response.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         response_text = response._result.candidates[0].content.parts[0].text
#         print("Response Text:", response_text)  # Debug print

#         # Parse the relevant portion
#         categories_data = []
#         lines = response_text.strip().split('\n')
#         for line in lines:
#             if ':' in line:
#                 try:
#                     name, amount_str = line.split(':')
#                     name = name.strip()
#                     amount = Decimal(amount_str.strip().strip('$'))
#                     categories_data.append({'name': name, 'amount': amount})
#                 except (InvalidOperation, AttributeError, ValueError) as e:
#                     print(f"Invalid amount format: {line} ({e})")
#                     continue

#         if not categories_data:
#             return Response({'detail': 'Error parsing Gemini response (no valid categories found).'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         total_amount = Decimal('0.00')
#         updated_categories = []

#         for category_data in categories_data:
#             name = category_data['name']
#             amount = category_data['amount']
#             total_amount += amount

#             # Check if the category already exists
#             existing_category = next((cat for cat in existing_categories if cat.name == name), None)
#             if existing_category:
#                 existing_category.amount = amount
#                 # Generate a unique description if it doesn't have one
#                 if not existing_category.description:
#                     existing_category.description = self.generate_description(name)
#                 updated_categories.append(existing_category)
#             else:
#                 updated_categories.append(Category(
#                     name=name,
#                     amount=amount,
#                     budget=budget,
#                     description=self.generate_description(name),
#                     created_at=date.today()
#                 ))

#         if total_amount > budget.total_expenses:
#             return Response({'detail': 'The total amount of categories exceeds the budget total expenses.'}, status=status.HTTP_400_BAD_REQUEST)

#         # Save updated categories
#         for category in updated_categories:
#             category.save()

#         return Response({'detail': 'Categories updated successfully.'}, status=status.HTTP_200_OK)

#     def generate_description(self, category_name):
#         prompt = f"Generate a unique description for a budget category named '{category_name}'."
#         response = genai.GenerativeModel('gemini-1.0-pro-latest').generate_content(prompt)
#         if not hasattr(response, '_result'):
#             return "No description available."
        
#         response_text = response._result.candidates[0].content.parts[0].text.strip()
#         return response_text if response_text else "No description available."




from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import date
from decimal import Decimal, InvalidOperation
import google.generativeai as genai







class CategoryCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        genai.configure(api_key=settings.GOOGLE_API_KEY)

    def post(self, request, *args, **kwargs):
        budget_id = request.data.get('budget')
        description = request.data.get('description')

        if not budget_id or not description:
            return Response({'detail': 'Budget and description are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            budget = Budget.objects.get(id=budget_id)
        except Budget.DoesNotExist:
            return Response({'detail': 'Budget not found.'}, status=status.HTTP_404_NOT_FOUND)

        if budget.income.user != request.user:
            return Response({'detail': 'You do not have permission to create categories for this budget.'}, status=status.HTTP_403_FORBIDDEN)

        # Fetch existing categories
        existing_categories = Category.objects.filter(budget=budget)
        existing_categories_text = "\n".join([f"{cat.name}: {cat.amount}" for cat in existing_categories])
        # print(f"these are the existing categories ....{existing_categories_text}") 
        total_amount = Decimal('0.00')
        categories_data = []

        while total_amount <= budget.total_expenses:
            model = genai.GenerativeModel('gemini-1.0-pro-latest')
            prompt = f"""Update the following budget categories based on the description: '{description}'. 
            Do not generate new categories unless explicitly specified. 
            Ensure the total amount does not exceed {budget.total_expenses}. This is a very strict command: do not
            spend beyond {budget.total_expenses}.

            Existing categories and amounts are:
            {existing_categories_text}

            **Note:** VERY VERY IMOORTANT TO READ THIS !!!!!!!!!!!!!!!!!!!!!To delete a category, append the word "DELETE" to its end (e.g., "TransportDELETE: Amount").

            **Note:** If there is any residual amount after updating existing categories, save it into a category called "Extra".

            Return the data in the following format:
            Category1: Amount1
            Category2: Amount2
            ...
            CategoryN: AmountN
            """
                        
            
            response = model.generate_content(prompt)

            # Extract the text part of the response
            if not hasattr(response, '_result'):
                return Response({'detail': 'Error parsing Gemini response.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            response_text = response._result.candidates[0].content.parts[0].text
            print("Response Text:", response_text)  # Debug print

            # Parse the relevant portion
            categories_data = []

            lines = response_text.strip().split('\n')
            for line in lines:
                if ':' in line:
                    try:
                        name, amount_str = line.split(':')
                        name = name.strip()
                        amount = Decimal(amount_str.strip().strip('$'))
                        categories_data.append({'name': name, 'amount': amount})
                    except (InvalidOperation, AttributeError, ValueError) as e:
                        print(f"Invalid amount format: {line} ({e})")
                        continue

            if not categories_data:
                return Response({'detail': 'Error parsing Gemini response (no valid categories found).'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            total_amount = sum([cat['amount'] for cat in categories_data])

            if total_amount == budget.total_expenses:
                break

        updated_categories = []
        marked_for_deletion = []

        # Identify categories to be deleted and updated
        for category_data in categories_data:
            name = category_data['name']
            amount = category_data['amount']
            if name.endswith('DELETE'):
                name = name.replace('DELETE', '').strip()
                category_data['name'] = name
                matching_category = next((cat for cat in existing_categories if cat.name == name), None)
                if matching_category:
                    matching_category.isDelete = True
                    marked_for_deletion.append(matching_category)
            else:
                matching_category = next((cat for cat in existing_categories if cat.name == name), None)
                if matching_category:
                    matching_category.amount = amount
                    if not matching_category.description:
                        matching_category.description = self.generate_description(name)
                    updated_categories.append(matching_category)
                else:
                    updated_categories.append(Category(
                        name=name,
                        amount=amount,
                        budget=budget,
                        description=self.generate_description(name),
                        created_at=date.today()
                    ))

        # Save updated categories and mark for deletion
        for category in marked_for_deletion:
            print(f"Marking category for deletion: {category.name}")  # Debug print
            category.save()
            self.handle_savings_deletion(request.user, category)
            category.delete()
        print(f"Number of categories marked for deletion: {len(marked_for_deletion)}")

        for category in updated_categories:
            category.save()

        # Handle savings updates
        self.handle_savings(request.user, categories_data)

        return Response({'detail': 'Categories updated successfully.'}, status=status.HTTP_200_OK)

    def generate_description(self, category_name):
        prompt = f"Generate a unique description for a budget category named '{category_name}'."
        response = genai.GenerativeModel('gemini-1.0-pro-latest').generate_content(prompt)
        if not hasattr(response, '_result'):
            return "No description available."
        
        response_text = response._result.candidates[0].content.parts[0].text.strip()
        return response_text if response_text else "No description available."

    def handle_savings(self, user, categories_data):
        # Fetch all savings for the user
        savings_objects = Savings.objects.filter(user=user)

        for category_data in categories_data:
            name = category_data['name']
            amount = category_data.get('amount', None)
            if 'savings' in name.lower():                # Check if a savings object with the same goal_name exists
                savings_object = next((s for s in savings_objects if s.goal_name == name), None)
                if savings_object:
                    # Update existing savings object
                    savings_object.amount_saved = amount
                    savings_object.description = self.generate_description(name)
                    savings_object.save()
                else:
                    # Create a new savings object
                    Savings.objects.create(
                        user=user,
                        goal_name=name,
                        target_amount=Decimal('0.00'),  # target_amount to be handled later
                        amount_saved=amount,
                        description=self.generate_description(name),
                        created_at=date.today(),
                        updated_at=date.today()
                    )

    def handle_savings_deletion(self, user, category):
        # Fetch the savings object
        savings_object = Savings.objects.filter(user=user, goal_name=category.name).first()
        if savings_object:
            savings_object.amount_saved -= category.amount
            savings_object.save()














class BudgetDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        try:
            budget = Budget.objects.get(pk=pk)
        except Budget.DoesNotExist:
            return Response({'detail': 'Budget not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        income = budget.income
        if income.user != request.user:
            return Response({'detail': 'You do not have permission to view this budget.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = BudgetSerializer(budget)
        return Response(serializer.data, status=status.HTTP_200_OK)




















class BudgetUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        try:
            budget = Budget.objects.get(pk=pk)
        except Budget.DoesNotExist:
            return Response({'detail': 'Budget not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        income = budget.income
        if income.user != request.user:
            return Response({'detail': 'You do not have permission to edit this budget.'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data.copy()
        
        # Only allow updates to 'name', 'end_date', and 'description'
        allowed_fields = ['name', 'end_date', 'description']
        for field in list(data.keys()):
            if field not in allowed_fields:
                data.pop(field)
        
        serializer = BudgetSerializer(budget, data=data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)










class UserIncomeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            income = Income.objects.get(id=pk)
        except Income.DoesNotExist:
            return Response({'detail': 'Income not found.'}, status=status.HTTP_404_NOT_FOUND)

        if income.user != request.user:
            raise PermissionDenied("You do not have permission to access this income entry.")

        budget = Budget.objects.get(income=income)
        categories = Category.objects.filter(budget=budget)

        income_serializer = IncomeSerializer(income, many=False)
        budget_serializer = BudgetSerializer(budget, many=False)
        categories_serializer = CategorySerializer(categories, many=True)

        response_data = {
            'income': income_serializer.data,
            'budget': budget_serializer.data,
            'categories': categories_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK) 





class CategoryUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            category = Category.objects.get(id=pk)
        except Category.DoesNotExist:
            return Response({'detail': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)

        budget = category.budget
        if budget.income.user != request.user:
            raise PermissionDenied("You do not have permission to update this category.")

        data = request.data
        category.name = data.get('name', category.name)
        category.description = data.get('description', category.description)
        category.save()

        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)









from decimal import Decimal, InvalidOperation
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class SavingsUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            savings = Savings.objects.get(id=pk)
        except Savings.DoesNotExist:
            return Response({'detail': 'Savings entry not found.'}, status=status.HTTP_404_NOT_FOUND)

        if savings.user != request.user:
            raise PermissionDenied("You do not have permission to update this savings entry.")

        data = request.data
        goal_name = data.get('goal_name', savings.goal_name)
        target_amount = data.get('target_amount', savings.target_amount)
        description = data.get('description', savings.description)

        # Ensure the goal name ends with 'Savings' or 'savings'
        if not (goal_name.endswith('Savings') or goal_name.endswith('savings')):
            goal_name += ' Savings'

        # Convert target_amount to Decimal if it's not None
        if target_amount is not None:
            try:
                target_amount = Decimal(target_amount)
            except InvalidOperation:
                return Response({'detail': 'Invalid target amount.'}, status=status.HTTP_400_BAD_REQUEST)

            if target_amount < savings.amount_saved:
                return Response({'detail': 'You can\'t set the target below the amount already saved.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a matching category exists and is owned by the same user
        matching_category = Category.objects.filter(
            budget__income__user=request.user,
            name=savings.goal_name
        ).first()

        if matching_category:
            matching_category.name = goal_name
            matching_category.save()

        savings.goal_name = goal_name
        savings.target_amount = target_amount
        savings.description = description
        savings.save()

        serializer = SavingsSerializer(savings)
        return Response(serializer.data, status=status.HTTP_200_OK)








class UserSavingsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SavingsSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        name = self.request.query_params.get('goal_name')
        savings = Savings.objects.filter(user=self.request.user)
        if name:
            savings = savings.filter(Q(goal_name__icontains=name))
        return savings

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)










class UserSavingsDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            savings = Savings.objects.get(id=pk)
        except Savings.DoesNotExist:
            return Response({'detail': 'Savings entry not found.'}, status=status.HTTP_404_NOT_FOUND)

        if savings.user != request.user:
            raise PermissionDenied("You do not have permission to access this savings entry.")

        serializer = SavingsSerializer(savings)
        return Response(serializer.data, status=status.HTTP_200_OK)



 

class SavingsDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            savings = Savings.objects.get(id=pk)
        except Savings.DoesNotExist:
            return Response({'detail': 'Savings entry not found.'}, status=status.HTTP_404_NOT_FOUND)

        if savings.user != request.user:
            raise PermissionDenied("You do not have permission to delete this savings entry.")

        goal_name = savings.goal_name

        # Find matching category
        matching_categories = Category.objects.filter(name=goal_name, budget__income__user=request.user)

        for category in matching_categories:
            budget = category.budget

            # Check for existing 'Extra' category in the same budget
            extra_category, created = Category.objects.get_or_create(
                budget=budget,
                name='Extra',
                defaults={'description': 'Extra funds', 'amount': Decimal('0.00')}
            )

            # Transfer amount from the matched category to the 'Extra' category
            extra_category.amount += category.amount
            extra_category.save()

            # Delete the matched category
            category.delete()

        # Finally, delete the savings object
        savings.delete()

        return Response({'detail': 'Savings and associated categories deleted successfully.'}, status=status.HTTP_200_OK)

