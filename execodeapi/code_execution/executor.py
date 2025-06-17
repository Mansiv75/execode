import subprocess
import tempfile
import os
import time
import signal
from django.conf import settings

class CodeExecutor:
    def __init__(self, code, language_slug, input_data="", timeout=5):
        self.code = code
        self.language_slug = language_slug
        self.input_data = input_data
        self.timeout = timeout
        
    def execute(self):
        """Execute code and return result"""
        try:
            if self.language_slug == 'python':
                return self._execute_python()
            elif self.language_slug == 'cpp':
                return self._execute_cpp()
            elif self.language_slug == 'java':
                return self._execute_java()
            else:
                return {
                    'status': 'Error',
                    'output': '',
                    'error': 'Unsupported language',
                    'execution_time': 0,
                    'memory_usage': 0
                }
        except Exception as e:
            return {
                'status': 'Error',
                'output': '',
                'error': str(e),
                'execution_time': 0,
                'memory_usage': 0
            }
    
    def _execute_python(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(self.code)
            temp_file = f.name
        
        try:
            start_time = time.time()
            result = subprocess.run(
                ['python3', temp_file],
                input=self.input_data,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            execution_time = time.time() - start_time
            
            if result.returncode == 0:
                return {
                    'status': 'Completed',
                    'output': result.stdout,
                    'error': result.stderr,
                    'execution_time': execution_time,
                    'memory_usage': 0  # Basic implementation
                }
            else:
                return {
                    'status': 'Error',
                    'output': result.stdout,
                    'error': result.stderr,
                    'execution_time': execution_time,
                    'memory_usage': 0
                }
        except subprocess.TimeoutExpired:
            return {
                'status': 'Timeout',
                'output': '',
                'error': 'Time limit exceeded',
                'execution_time': self.timeout,
                'memory_usage': 0
            }
        finally:
            os.unlink(temp_file)
    
    def _execute_cpp(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as f:
            f.write(self.code)
            cpp_file = f.name
        
        exe_file = f"{cpp_file}.out"
        
        try:
            compile_result = self._compile_cpp(cpp_file, exe_file)
            return (
                {
                    'status': 'Error',
                    'output': '',
                    'error': f'Compilation Error: {compile_result.stderr}',
                    'execution_time': 0,
                    'memory_usage': 0
                }
                if compile_result.returncode != 0 else
                self._run_cpp_executable(exe_file)
            )
                
        except subprocess.TimeoutExpired:
            return {
                'status': 'Timeout',
                'output': '',
                'error': 'Time limit exceeded',
                'execution_time': self.timeout,
                'memory_usage': 0
            }
        finally:
            for file_path in [cpp_file, exe_file]:
                if os.path.exists(file_path):
                    os.unlink(file_path)
    
    def _compile_java(self, java_file):
        """Compile Java file and return the result."""
        return subprocess.run(
            ['javac', java_file],
            capture_output=True,
            text=True,
            timeout=10
        )

    def _execute_java(self):
        # Extract class name from code
        import re
        class_match = re.search(r'public\s+class\s+(\w+)', self.code)
        if not class_match:
            return {
                'status': 'Error',
                'output': '',
                'error': 'No public class found',
                'execution_time': 0,
                'memory_usage': 0
            }
        
        class_name = class_match.group(1)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            java_file = os.path.join(temp_dir, f'{class_name}.java')
            
            with open(java_file, 'w') as f:
                f.write(self.code)
            
            try:
                compile_result = self._compile_java(java_file)
                return (
                    {
                        'status': 'Error',
                        'output': '',
                        'error': f'Compilation Error: {compile_result.stderr}',
                        'execution_time': 0,
                        'memory_usage': 0
                    }
                    if compile_result.returncode != 0 else
                    self._run_java_class(temp_dir, class_name)
                )
            except subprocess.TimeoutExpired:
                return {
                    'status': 'Timeout',
                    'output': '',
                    'error': 'Time limit exceeded',
                    'execution_time': self.timeout,
                    'memory_usage': 0
                }

    def _run_java_class(self, temp_dir, class_name):
        start_time = time.time()
        result = subprocess.run(
            ['java', '-cp', temp_dir, class_name],
            input=self.input_data,
            capture_output=True,
            text=True,
            timeout=self.timeout
        )
        execution_time = time.time() - start_time
        return (
            {
                'status': 'Completed',
                'output': result.stdout,
                'error': result.stderr,
                'execution_time': execution_time,
                'memory_usage': 0
            }
            if result.returncode == 0 else
            {
                'status': 'Error',
                'output': result.stdout,
                'error': result.stderr,
                'execution_time': execution_time,
                'memory_usage': 0
            }
        )