/**
 * Template: Use Case
 * 
 * Use Cases orquestram a execução de lógica de aplicação.
 * 
 * Regras:
 * - Um use case = Uma operação de negócio
 * - Recebe DTO de entrada, retorna DTO de saída
 * - Orquestra entidades e repositórios
 * - NÃO contém lógica de negócio (isso vai no Domain)
 * - Usa injeção de dependência
 */

import { UseCase } from '@core/application/base/use-case.base';
import { Result } from '@core/application/base/result';

// Importar do Domain
import { /* Entity */ } from '../../domain/entities';
import { /* Repository */ } from '../../domain/repositories';

// DTOs
export interface __USE_CASE_NAME__Input {
  // Propriedades de entrada
  // id: string;
  // name: string;
}

export interface __USE_CASE_NAME__Output {
  // Propriedades de saída
  // id: string;
  // name: string;
  // createdAt: Date;
}

// Erros específicos do use case
export class __USE_CASE_NAME__Error extends Error {
  constructor(message: string) {
    super(message);
    this.name = '__USE_CASE_NAME__Error';
  }
}

export class __USE_CASE_NAME__
  implements UseCase<__USE_CASE_NAME__Input, Result<__USE_CASE_NAME__Output>>
{
  // ==========================================
  // Injeção de Dependências
  // ==========================================
  
  constructor(
    // private readonly repository: __Entity__Repository,
    // private readonly eventBus: EventBus,
  ) {}
  
  // ==========================================
  // Execução
  // ==========================================
  
  async execute(
    input: __USE_CASE_NAME__Input,
  ): Promise<Result<__USE_CASE_NAME__Output>> {
    try {
      // 1. Validar input (validações de aplicação)
      // if (!input.id) {
      //   return Result.fail('ID is required');
      // }
      
      // 2. Buscar/Criar entidades
      // const entity = await this.repository.findById(input.id);
      // if (!entity) {
      //   return Result.fail('Entity not found');
      // }
      
      // 3. Executar operação no domínio
      // entity.doSomething();
      
      // 4. Persistir
      // await this.repository.save(entity);
      
      // 5. Publicar eventos (se necessário)
      // await this.eventBus.publishAll(entity.domainEvents);
      
      // 6. Retornar resultado
      return Result.ok({
        // id: entity.id.toString(),
        // name: entity.name,
        // createdAt: entity.createdAt,
      });
      
    } catch (error) {
      // Log do erro (usar logger injetado em produção)
      console.error('Error in __USE_CASE_NAME__:', error);
      
      // Retornar falha
      return Result.fail(
        error instanceof Error ? error.message : 'Unknown error',
      );
    }
  }
}

// ============================================
// Exemplo de Use Case Completo
// ============================================

/*
export interface CreateOrderInput {
  userId: string;
  items: Array<{
    productId: string;
    quantity: number;
  }>;
}

export interface CreateOrderOutput {
  orderId: string;
  total: number;
  status: string;
}

export class CreateOrderUseCase
  implements UseCase<CreateOrderInput, Result<CreateOrderOutput>>
{
  constructor(
    private readonly orderRepository: OrderRepository,
    private readonly productRepository: ProductRepository,
    private readonly eventBus: EventBus,
  ) {}

  async execute(input: CreateOrderInput): Promise<Result<CreateOrderOutput>> {
    // 1. Validar usuário existe
    // 2. Buscar produtos
    const products = await Promise.all(
      input.items.map(item => this.productRepository.findById(item.productId))
    );
    
    if (products.some(p => !p)) {
      return Result.fail('One or more products not found');
    }
    
    // 3. Criar order (lógica no domínio)
    const order = Order.create({
      userId: UserId.create(input.userId),
      items: input.items.map((item, i) => 
        OrderItem.create(products[i]!, item.quantity)
      ),
    });
    
    // 4. Persistir
    await this.orderRepository.save(order);
    
    // 5. Publicar eventos
    await this.eventBus.publishAll(order.domainEvents);
    
    // 6. Retornar
    return Result.ok({
      orderId: order.id.toString(),
      total: order.total.amount,
      status: order.status.toString(),
    });
  }
}
*/
